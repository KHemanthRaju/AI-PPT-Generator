import streamlit as st
import requests
import json
import re
import PyPDF2
from docx import Document
import io

# Page config
st.set_page_config(page_title="AI PPT Generator Chatbot", page_icon="🤖", layout="wide")

# Helper functions for text extraction
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    try:
        doc = Document(io.BytesIO(docx_file.read()))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {str(e)}")
        return None

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "waiting_for_urls" not in st.session_state:
    st.session_state.waiting_for_urls = False
if "topic" not in st.session_state:
    st.session_state.topic = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "uploaded_document" not in st.session_state:
    st.session_state.uploaded_document = None
if "document_text" not in st.session_state:
    st.session_state.document_text = None
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Theme configuration - WCAG AA compliant colors
THEME_COLORS = {
    "light": {
        "bg": "#ffffff",
        "secondary_bg": "#f8f9fa",
        "text": "#1a1a1a",
        "text_secondary": "#4a4a4a",
        "border": "#e0e0e0",
        "primary": "#667eea",
        "success": "#11998e",
    },
    "dark": {
        "bg": "#1e1e1e",
        "secondary_bg": "#2d2d2d",
        "text": "#e8e8e8",
        "text_secondary": "#b8b8b8",
        "border": "#404040",
        "primary": "#7b8ff5",
        "success": "#38ef7d",
    }
}

theme = THEME_COLORS[st.session_state.theme]

# Apply theme CSS
st.markdown(f"""
<style>
    /* Main container */
    .main {{
        background-color: {theme['bg']};
        color: {theme['text']};
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {theme['secondary_bg']};
        border-right: 1px solid {theme['border']};
    }}

    /* Text elements */
    h1, h2, h3, h4, h5, h6 {{
        color: {theme['text']} !important;
    }}

    p, label, span {{
        color: {theme['text_secondary']} !important;
    }}

    /* Chat messages */
    .stChatMessage {{
        background-color: {theme['secondary_bg']};
        border: 1px solid {theme['border']};
    }}

    /* Input fields */
    .stTextInput input, .stChatInput input {{
        background-color: {theme['secondary_bg']};
        color: {theme['text']};
        border-color: {theme['border']};
    }}

    /* File uploader */
    [data-testid="stFileUploader"] {{
        background-color: {theme['secondary_bg']};
        border-color: {theme['border']};
    }}

    /* Buttons */
    .stButton>button {{
        background: linear-gradient(135deg, {theme['primary']} 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }}

    /* Slider */
    .stSlider {{
        color: {theme['primary']};
    }}

    /* Success messages */
    .success {{
        background-color: {theme['success']};
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {theme['secondary_bg']};
        color: {theme['text']};
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 AI PowerPoint Generator Chatbot")
st.markdown("### Chat with me to create amazing presentations!")

# Sidebar
with st.sidebar:
    # Theme toggle button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("## 🎨 Theme")
    with col2:
        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(theme_icon, key="theme_toggle", help="Toggle dark/light mode"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()

    st.markdown("---")

    st.markdown("## 📖 About")
    with st.expander("ℹ️ Click to learn more"):
        st.markdown("""
        **AI PPT Generator**

        Powered by Claude Sonnet 4.5 AI

        **Features:**
        - 🌐 Web content extraction
        - 📊 Excel/CSV chart generation
        - 📄 PDF/DOC conversion
        - 🖼️ Image analysis
        - 🔗 Automatic URL crawling

        **Created by:** Hemanth Raju K
        """)

    st.markdown("## ⚙️ Settings")
    slide_count = st.slider(
        "Slides",
        min_value=3,
        max_value=15,
        value=6,
        step=1
    )

    st.markdown("## 📎 Upload Files")
    uploaded_file = st.file_uploader(
        "Excel/CSV (for charts)",
        type=['csv', 'xlsx', 'xls']
    )

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.success("✅ Data file ready")
    else:
        st.session_state.uploaded_file = None

    uploaded_document = st.file_uploader(
        "PDF/DOC (for content)",
        type=['pdf', 'doc', 'docx']
    )

    if uploaded_document is not None:
        st.session_state.uploaded_document = uploaded_document

        # Extract text based on file type
        with st.spinner("Extracting..."):
            file_extension = uploaded_document.name.split('.')[-1].lower()

            if file_extension == 'pdf':
                text = extract_text_from_pdf(uploaded_document)
            elif file_extension in ['doc', 'docx']:
                text = extract_text_from_docx(uploaded_document)
            else:
                text = None
                st.error("Unsupported format")

            if text:
                st.session_state.document_text = text
                # Check for URLs silently
                url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
                found_urls = re.findall(url_pattern, text)
                unique_urls = list(set([url.rstrip('.,;:!?)') for url in found_urls]))

                if unique_urls:
                    st.success(f"✅ Document ready ({len(unique_urls)} link(s) found)")
                else:
                    st.success("✅ Document ready")
            else:
                st.session_state.document_text = None
    else:
        st.session_state.uploaded_document = None
        st.session_state.document_text = None

    if st.button("🔄 Start New Conversation"):
        st.session_state.messages = []
        st.session_state.waiting_for_urls = False
        st.session_state.topic = None
        st.session_state.uploaded_file = None
        st.session_state.uploaded_document = None
        st.session_state.document_text = None
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "download_url" in message:
            st.markdown(message["content"])
            st.markdown(f"### [📥 Download Your Presentation]({message['download_url']})")
            if "pptx_info" in message:
                info = message["pptx_info"]
                st.success(f"""
                ✅ **Presentation Ready!**
                - 📊 Slides: {info.get('slide_count', 'N/A')}
                - 🖼️ Images Processed: {info.get('images_processed', 0)}
                - 📎 Images Inserted: {info.get('images_inserted', 0)}
                - 💾 Size: {info.get('size_bytes', 0):,} bytes
                """)
        else:
            st.markdown(message["content"])

# Initial greeting
if len(st.session_state.messages) == 0:
    greeting = """
    👋 **Welcome! I create professional presentations for you.**

    Just tell me your topic, and I'll:
    - Search the web for content
    - Generate slides with insights
    - Add charts from your data (if uploaded)
    - Extract content from documents (if uploaded)

    **Get started:** Type your presentation topic below!

    *Example: "Create a presentation about AI trends"*
    """
    st.session_state.messages.append({"role": "assistant", "content": greeting})
    with st.chat_message("assistant"):
        st.markdown(greeting)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process based on conversation state
    if not st.session_state.waiting_for_urls:
        # User is providing the topic
        st.session_state.topic = prompt
        st.session_state.waiting_for_urls = True

        response = f"""
        Creating presentation: **"{prompt}"**

        **Next step:**
        - Type **"search"** to auto-find content
        - Or provide specific URLs

        *Recommended: Type "search"*
        """
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

    else:
        # User is providing URLs or choosing auto-search
        user_input_lower = prompt.lower().strip()

        # Check if user wants auto-search
        if any(keyword in user_input_lower for keyword in ['search', 'auto', 'automatic', 'find', 'lookup', 'google']):
            # User chose auto-search
            urls = []  # Empty list will trigger auto-search in backend

            response_msg = "🔍 Searching and generating..."
            st.session_state.messages.append({"role": "assistant", "content": response_msg})
            with st.chat_message("assistant"):
                st.markdown(response_msg)
        else:
            # Extract URLs from the message
            url_pattern = r'https?://[^\s,]+'
            urls = re.findall(url_pattern, prompt)

            # Also try splitting by lines
            lines = [line.strip() for line in prompt.split('\n') if line.strip()]
            for line in lines:
                if line.startswith('http'):
                    if line not in urls:
                        urls.append(line)

        if urls is None or (not any(keyword in user_input_lower for keyword in ['search', 'auto', 'automatic', 'find', 'lookup', 'google']) and len(urls) == 0):
            response = "⚠️ Please type **'search'** or provide URLs"
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        else:
            # Generate presentation
            with st.chat_message("assistant"):
                with st.spinner("⏳ Generating presentation..."):
                    try:
                        # Call API
                        api_url = "https://lorf2f330g.execute-api.us-west-2.amazonaws.com/prod/generate-ppt"

                        request_data = {
                            "description": st.session_state.topic,
                            "urls": urls,
                            "slide_count": slide_count
                        }

                        # Add document text if available (base64 encoded to avoid JSON encoding issues)
                        if st.session_state.document_text:
                            import base64
                            # Base64 encode the document text to avoid special character issues in JSON
                            document_text_bytes = st.session_state.document_text.encode('utf-8')
                            document_text_b64 = base64.b64encode(document_text_bytes).decode('utf-8')

                            # Check size (API Gateway has 10MB limit)
                            text_size_mb = len(document_text_b64) / (1024 * 1024)
                            if text_size_mb > 8:  # Leave some room for other request data
                                error_msg = f"""⚠️ **Document text is too large ({text_size_mb:.2f}MB)**

API Gateway has a 10MB payload limit. Your document text is too large to send directly.

**Please:**
- Try a shorter document (fewer pages)
- Or extract only relevant sections
- Or use URL-only mode without document upload

**Document size:** {text_size_mb:.2f}MB (limit: ~8MB)"""
                                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                                st.error(error_msg)
                                st.session_state.waiting_for_urls = False
                                st.session_state.topic = None
                                st.stop()

                            request_data['document_text_b64'] = document_text_b64

                        # Add uploaded file data if available
                        if st.session_state.uploaded_file is not None:
                            import base64

                            # Reset file pointer to beginning
                            st.session_state.uploaded_file.seek(0)
                            file_bytes = st.session_state.uploaded_file.read()
                            file_extension = '.' + st.session_state.uploaded_file.name.split('.')[-1]

                            # Check file size (limit to 3MB to account for base64 encoding overhead)
                            file_size_mb = len(file_bytes) / (1024 * 1024)

                            if file_size_mb > 3:
                                error_msg = f"⚠️ File too large ({file_size_mb:.1f}MB). Max: 3MB"
                                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                                st.error(error_msg)
                                st.session_state.waiting_for_urls = False
                                st.session_state.topic = None
                                st.stop()

                            file_b64 = base64.b64encode(file_bytes).decode('utf-8')

                            request_data['csv_data'] = file_b64
                            request_data['file_extension'] = file_extension

                        response = requests.post(
                            api_url,
                            json=request_data,
                            headers={'Content-Type': 'application/json'},
                            timeout=120
                        )

                        if response.status_code == 200:
                            result = response.json()

                            if 'download_url' in result:
                                info = result.get('pptx_info', {})
                                success_msg = f"✅ **Presentation ready!** ({info.get('slide_count', 'N/A')} slides)"

                                st.session_state.messages.append({
                                    "role": "assistant",
                                    "content": success_msg,
                                    "download_url": result['download_url'],
                                    "pptx_info": info
                                })

                                st.markdown(success_msg)
                                st.markdown(f"### [📥 Download Presentation]({result['download_url']})")
                            else:
                                error_msg = "❌ No download link received"
                                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                                st.error(error_msg)
                        else:
                            error_msg = f"❌ Server error ({response.status_code})"
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                            st.error(error_msg)

                        # Reset state for new conversation
                        st.session_state.waiting_for_urls = False
                        st.session_state.topic = None

                    except requests.Timeout:
                        error_msg = "⏱️ Request timed out. Try again."
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.error(error_msg)
                        st.session_state.waiting_for_urls = False
                        st.session_state.topic = None

                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.error(error_msg)
                        st.session_state.waiting_for_urls = False
                        st.session_state.topic = None

# Footer
st.markdown("---")
st.caption("💡 Use 'Start New Conversation' button in sidebar to reset")
