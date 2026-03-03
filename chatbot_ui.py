import streamlit as st
import requests
import json
import re
import PyPDF2
from docx import Document
import io

# Page config with custom styling
st.set_page_config(
    page_title="AI PPT Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI/UX with theme support
st.markdown(f"""
<style>
    /* Main container styling */
    .main {{
        background: {theme['bg_primary']};
        padding: 0;
        transition: background 0.3s ease;
    }}

    /* Chat container */
    .stChatMessage {{
        background-color: {theme['chat_bg']};
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 10px {theme['card_shadow']};
        transition: all 0.3s ease;
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: {theme['sidebar_bg']};
        border-right: 2px solid {theme['border_color']};
        transition: all 0.3s ease;
    }}

    /* File uploader styling */
    [data-testid="stFileUploader"] {{
        background-color: {theme['bg_secondary']};
        border-radius: 10px;
        padding: 15px;
        border: 2px dashed {theme['accent_color']};
        transition: all 0.3s ease;
    }}

    /* Button styling */
    .stButton>button {{
        background: linear-gradient(135deg, {theme['bg_gradient_start']} 0%, {theme['bg_gradient_end']} 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }}

    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }}

    /* Success message styling */
    .success-box {{
        background: linear-gradient(135deg, {theme['success_gradient_start']} 0%, {theme['success_gradient_end']} 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        transition: all 0.3s ease;
    }}

    /* Info box styling - WCAG AA compliant white text on gradient */
    .info-box {{
        background: linear-gradient(135deg, {theme['bg_gradient_start']} 0%, {theme['bg_gradient_end']} 100%);
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        transition: all 0.3s ease;
    }}

    .info-box h2 {{
        color: #FFFFFF !important;
    }}

    .info-box p {{
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 1.1em !important;
        line-height: 1.8 !important;
    }}

    .info-box strong {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }}

    /* Step indicator */
    .step-indicator {{
        display: flex;
        justify-content: space-between;
        margin: 30px 0;
    }}

    .step {{
        flex: 1;
        text-align: center;
        padding: 15px;
        background: {theme['bg_secondary']};
        margin: 0 10px;
        border-radius: 10px;
        box-shadow: 0 2px 10px {theme['card_shadow']};
        transition: all 0.3s ease;
    }}

    .step.active {{
        background: linear-gradient(135deg, {theme['bg_gradient_start']} 0%, {theme['bg_gradient_end']} 100%);
        color: white;
    }}

    /* Stats card */
    .stats-card {{
        background: {theme['bg_secondary']};
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 10px {theme['card_shadow']};
        text-align: center;
        color: {theme['text_primary']};
        transition: all 0.3s ease;
    }}

    .stats-card h3 {{
        color: {theme['text_primary']} !important;
        margin: 10px 0;
        font-weight: 700;
    }}

    .stats-card p {{
        color: {theme['text_secondary']} !important;
        font-size: 0.95em;
        font-weight: 500;
    }}

    /* Header styling */
    h1 {{
        background: linear-gradient(135deg, {theme['bg_gradient_start']} 0%, {theme['bg_gradient_end']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em !important;
        font-weight: 800 !important;
        margin-bottom: 10px !important;
    }}

    /* Quick action buttons - WCAG AA compliant */
    .quick-action {{
        background: {theme['bg_secondary']};
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid {theme['border_color']};
        color: {theme['text_primary']};
        font-weight: 500;
    }}

    .quick-action:hover {{
        border-color: {theme['accent_color']};
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        transform: translateX(5px);
    }}

    .quick-action strong {{
        color: {theme['accent_color']} !important;
        font-weight: 700 !important;
    }}

    /* General text styling for WCAG AA compliance */
    h2, h3, h4 {{
        color: {theme['text_primary']} !important;
        font-weight: 700;
    }}

    p {{
        color: {theme['text_secondary']} !important;
        font-weight: 500;
    }}

    .stMarkdown {{
        color: {theme['text_primary']};
    }}

    /* Fix header subtitle */
    .main h1 + p {{
        color: {theme['text_tertiary']} !important;
        font-weight: 600;
    }}

    /* Chat input placeholder - high contrast */
    .stChatInput input::placeholder {{
        color: {theme['text_tertiary']} !important;
        font-weight: 500;
    }}

    .stChatInput input {{
        background-color: {theme['bg_secondary']} !important;
        color: {theme['text_primary']} !important;
        border-color: {theme['border_color']} !important;
    }}

    /* Slider styling - professional blue instead of red */
    .stSlider [data-baseweb="slider"] [role="slider"] {{
        background-color: {theme['accent_color']} !important;
    }}

    .stSlider [data-baseweb="slider"] [data-testid="stTickBar"] > div {{
        background-color: {theme['accent_color']} !important;
    }}

    /* Sidebar text contrast */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {{
        color: {theme['text_primary']} !important;
        font-weight: 500;
    }}

    [data-testid="stSidebar"] small {{
        color: {theme['text_tertiary']} !important;
        font-weight: 500;
    }}

    /* Success box - ensure white text */
    .success-box {{
        background: linear-gradient(135deg, {theme['success_gradient_start']} 0%, {theme['success_gradient_end']} 100%);
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
    }}

    .success-box h2,
    .success-box p,
    .success-box strong {{
        color: #FFFFFF !important;
    }}

    /* Theme toggle button */
    .theme-toggle {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        background: {theme['bg_secondary']};
        border: 2px solid {theme['border_color']};
        border-radius: 50px;
        padding: 10px 20px;
        cursor: pointer;
        box-shadow: 0 2px 10px {theme['card_shadow']};
        transition: all 0.3s ease;
        font-size: 1.2em;
    }}

    .theme-toggle:hover {{
        transform: scale(1.1);
        box-shadow: 0 4px 15px {theme['card_shadow']};
    }}

</style>
""", unsafe_allow_html=True)

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
        st.error(f"❌ Error extracting text from PDF: {str(e)}")
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
        st.error(f"❌ Error extracting text from DOCX: {str(e)}")
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
if "current_step" not in st.session_state:
    st.session_state.current_step = 1
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Theme colors configuration
THEMES = {
    "light": {
        "bg_primary": "#f8f9fa",
        "bg_secondary": "#ffffff",
        "bg_gradient_start": "#667eea",
        "bg_gradient_end": "#764ba2",
        "text_primary": "#1a1a1a",
        "text_secondary": "#4a4a4a",
        "text_tertiary": "#5a5a5a",
        "border_color": "#e0e0e0",
        "chat_bg": "#ffffff",
        "sidebar_bg": "#ffffff",
        "card_shadow": "rgba(0,0,0,0.1)",
        "accent_color": "#667eea",
        "success_gradient_start": "#11998e",
        "success_gradient_end": "#38ef7d",
    },
    "dark": {
        "bg_primary": "#1a1a1a",
        "bg_secondary": "#2a2a2a",
        "bg_gradient_start": "#667eea",
        "bg_gradient_end": "#764ba2",
        "text_primary": "#e8e8e8",
        "text_secondary": "#b8b8b8",
        "text_tertiary": "#999999",
        "border_color": "#404040",
        "chat_bg": "#2a2a2a",
        "sidebar_bg": "#242424",
        "card_shadow": "rgba(0,0,0,0.3)",
        "accent_color": "#7b8ff5",
        "success_gradient_start": "#11998e",
        "success_gradient_end": "#38ef7d",
    }
}

# Get current theme colors
theme = THEMES[st.session_state.theme]

# Header with better design
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h1 style='text-align: center;'>🎯 AI PowerPoint Generator</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 1.2em; color: {theme['text_secondary']};'>Transform your ideas into professional presentations instantly</p>", unsafe_allow_html=True)

# Sidebar with improved organization
with st.sidebar:
    # Theme toggle at the top
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🚀 Quick Start")
    with col2:
        theme_icon = "🌙" if st.session_state.theme == "light" else "☀️"
        if st.button(theme_icon, key="theme_toggle", help="Toggle light/dark theme"):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()

    # Step indicator in sidebar
    current_step = st.session_state.current_step
    active_color = theme['accent_color']
    inactive_bg = theme['border_color']
    inactive_text = theme['text_tertiary']
    step_bg = theme['bg_secondary']

    st.markdown(f"""
    <div style='background: {step_bg}; padding: 15px; border-radius: 10px; margin: 10px 0; border: 1px solid {theme["border_color"]};'>
        <div style='display: flex; align-items: center; margin: 10px 0;'>
            <div style='width: 30px; height: 30px; border-radius: 50%; background: {active_color if current_step >= 1 else inactive_bg}; color: white; display: flex; align-items: center; justify-content: center; margin-right: 10px; font-weight: bold;'>1</div>
            <span style='color: {active_color if current_step >= 1 else inactive_text}; font-weight: {"bold" if current_step == 1 else "normal"};'>Upload Files (Optional)</span>
        </div>
        <div style='display: flex; align-items: center; margin: 10px 0;'>
            <div style='width: 30px; height: 30px; border-radius: 50%; background: {active_color if current_step >= 2 else inactive_bg}; color: white; display: flex; align-items: center; justify-content: center; margin-right: 10px; font-weight: bold;'>2</div>
            <span style='color: {active_color if current_step >= 2 else inactive_text}; font-weight: {"bold" if current_step == 2 else "normal"};'>Enter Topic</span>
        </div>
        <div style='display: flex; align-items: center; margin: 10px 0;'>
            <div style='width: 30px; height: 30px; border-radius: 50%; background: {active_color if current_step >= 3 else inactive_bg}; color: white; display: flex; align-items: center; justify-content: center; margin-right: 10px; font-weight: bold;'>3</div>
            <span style='color: {active_color if current_step >= 3 else inactive_text}; font-weight: {"bold" if current_step == 3 else "normal"};'>Generate & Download</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Settings section
    st.markdown("### ⚙️ Presentation Settings")
    slide_count = st.slider(
        "📊 Number of Slides",
        min_value=3,
        max_value=15,
        value=6,
        step=1,
        help="Choose how many slides you want in your presentation"
    )

    st.markdown(f"<div style='text-align: center; color: #667eea; font-size: 1.2em; font-weight: bold;'>{slide_count} slides</div>", unsafe_allow_html=True)

    st.markdown("---")

    # File upload section with better design
    st.markdown("### 📂 Upload Files (Optional)")

    # Data file uploader
    with st.expander("📊 Excel/CSV for Charts", expanded=False):
        st.markdown("<small>Upload data files to generate charts automatically</small>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose file",
            type=['csv', 'xlsx', 'xls'],
            key="data_file",
            label_visibility="collapsed"
        )

        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            st.success(f"✅ {uploaded_file.name}")
            file_size = len(uploaded_file.getvalue()) / 1024
            st.caption(f"📦 Size: {file_size:.1f} KB")
        else:
            st.session_state.uploaded_file = None

    # Document uploader
    with st.expander("📄 PDF/DOC for Content", expanded=False):
        st.markdown("<small>Upload documents to extract content and URLs</small>", unsafe_allow_html=True)
        uploaded_document = st.file_uploader(
            "Choose document",
            type=['pdf', 'doc', 'docx'],
            key="doc_file",
            label_visibility="collapsed"
        )

        if uploaded_document is not None:
            st.session_state.uploaded_document = uploaded_document

            # Extract text based on file type
            with st.spinner("📖 Extracting content..."):
                file_extension = uploaded_document.name.split('.')[-1].lower()

                if file_extension == 'pdf':
                    text = extract_text_from_pdf(uploaded_document)
                elif file_extension in ['doc', 'docx']:
                    text = extract_text_from_docx(uploaded_document)
                else:
                    text = None
                    st.error("❌ Unsupported format")

                if text:
                    st.session_state.document_text = text
                    # Check for URLs
                    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
                    found_urls = re.findall(url_pattern, text)
                    unique_urls = list(set([url.rstrip('.,;:!?)') for url in found_urls]))

                    st.success(f"✅ {uploaded_document.name}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.caption(f"📝 {len(text.split())} words")
                    with col2:
                        if unique_urls:
                            st.caption(f"🔗 {len(unique_urls)} links")
                else:
                    st.session_state.document_text = None
        else:
            st.session_state.uploaded_document = None
            st.session_state.document_text = None

    st.markdown("---")

    # About section
    with st.expander("ℹ️ About & Features"):
        st.markdown("""
        **Powered by Claude Sonnet 4.5 AI**

        **✨ Features:**
        - 🌐 Smart web search
        - 📊 Automated charts
        - 📄 Document conversion
        - 🖼️ Image analysis
        - 🔗 URL crawling
        - 🎨 Professional design

        **👨‍💻 Created by:**
        Hemanth Raju K

        **🎓 Arizona State University**
        MS Computer Science
        """)

    st.markdown("---")

    # Reset button with better design
    if st.button("🔄 New Presentation", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.waiting_for_urls = False
        st.session_state.topic = None
        st.session_state.uploaded_file = None
        st.session_state.uploaded_document = None
        st.session_state.document_text = None
        st.session_state.current_step = 1
        st.rerun()

# Main content area
if len(st.session_state.messages) == 0:
    # Welcome screen with better design
    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='stats-card'>
            <div style='font-size: 3em;'>🎨</div>
            <h3>Professional Design</h3>
            <p style='color: #666;'>Clean, modern slides with perfect formatting</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='stats-card'>
            <div style='font-size: 3em;'>⚡</div>
            <h3>Lightning Fast</h3>
            <p style='color: #666;'>Generate presentations in under 60 seconds</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='stats-card'>
            <div style='font-size: 3em;'>🤖</div>
            <h3>AI Powered</h3>
            <p style='color: #666;'>Smart content with Claude Sonnet 4.5</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick start guide
    st.markdown("""
    <div class='info-box'>
        <h2 style='color: white; margin-top: 0;'>👋 Welcome! Let's Create Your Presentation</h2>
        <p style='font-size: 1.1em; line-height: 1.8;'>
            <strong>Step 1:</strong> (Optional) Upload Excel/CSV for charts or PDF/DOC for content<br>
            <strong>Step 2:</strong> Type your presentation topic below<br>
            <strong>Step 3:</strong> Type "search" to generate automatically<br>
            <strong>Step 4:</strong> Download your professional presentation!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Example topics
    st.markdown("### 💡 Example Topics")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='quick-action'>
            <strong>🚀 Business:</strong> "Quarterly Sales Report"<br>
            <strong>🎓 Education:</strong> "Machine Learning Basics"<br>
            <strong>💼 Professional:</strong> "Project Status Update"
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='quick-action'>
            <strong>🔬 Research:</strong> "Climate Change Impact"<br>
            <strong>💻 Tech:</strong> "AI Trends in 2026"<br>
            <strong>📊 Analytics:</strong> "Market Analysis Report"
        </div>
        """, unsafe_allow_html=True)

    # Initial greeting message
    greeting = """
    👋 **Ready to get started?**

    Just type your presentation topic in the chat box below!

    *Example: "Create a presentation about AI trends in healthcare"*
    """
    st.session_state.messages.append({"role": "assistant", "content": greeting})

# Display chat history with better formatting
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        if message["role"] == "assistant" and "download_url" in message:
            st.markdown(message["content"])

            # Enhanced download section
            st.markdown("""
            <div class='success-box'>
                <h2 style='color: white; margin: 0;'>🎉 Your Presentation is Ready!</h2>
            </div>
            """, unsafe_allow_html=True)

            # Download button with stats
            if "pptx_info" in message:
                info = message["pptx_info"]

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Slides", info.get('slide_count', 'N/A'))
                with col2:
                    st.metric("🖼️ Images", info.get('images_inserted', 0))
                with col3:
                    size_kb = info.get('size_bytes', 0) / 1024
                    st.metric("💾 Size", f"{size_kb:.0f} KB")
                with col4:
                    st.markdown("<br>", unsafe_allow_html=True)

            st.markdown(f"""
            <a href="{message['download_url']}" target="_blank">
                <button style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; border: none; border-radius: 25px; padding: 15px 40px; font-size: 1.2em; font-weight: bold; cursor: pointer; width: 100%; margin: 20px 0; box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);'>
                    📥 Download Your Presentation
                </button>
            </a>
            """, unsafe_allow_html=True)

            st.success("✅ Click the button above to download your PowerPoint file")

        else:
            st.markdown(message["content"])

# Chat input with placeholder
if prompt := st.chat_input("💬 Type your presentation topic here...", key="chat_input"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Process based on conversation state
    if not st.session_state.waiting_for_urls:
        # User is providing the topic
        st.session_state.topic = prompt
        st.session_state.waiting_for_urls = True
        st.session_state.current_step = 2

        response = f"""
        **✅ Great! Creating presentation about:** "{prompt}"

        **📝 Next step:**

        Simply type **"search"** and I'll automatically:
        - 🔍 Search the web for relevant content
        - 📊 Generate professional slides
        - 🖼️ Add images and charts
        - 🎨 Apply beautiful formatting

        **Or** provide specific URLs if you have them.

        💡 *Recommended: Just type "search" for best results!*
        """
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(response)

    else:
        # User is providing URLs or choosing auto-search
        user_input_lower = prompt.lower().strip()

        # Check if user wants auto-search
        if any(keyword in user_input_lower for keyword in ['search', 'auto', 'automatic', 'find', 'lookup', 'google', 'generate']):
            # User chose auto-search
            urls = []  # Empty list will trigger auto-search in backend
            st.session_state.current_step = 3

            response_msg = "🔍 **Searching and generating your presentation...**\n\nThis will take about 30-60 seconds. Please wait!"
            st.session_state.messages.append({"role": "assistant", "content": response_msg})
            with st.chat_message("assistant", avatar="🤖"):
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

        if urls is None or (not any(keyword in user_input_lower for keyword in ['search', 'auto', 'automatic', 'find', 'lookup', 'google', 'generate']) and len(urls) == 0):
            response = """
            ⚠️ **Please choose an option:**

            - Type **"search"** to auto-generate (recommended)
            - Or paste specific URLs you want to use

            💡 *Tip: Just type "search" for the best experience!*
            """
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(response)
        else:
            # Generate presentation
            with st.chat_message("assistant", avatar="🤖"):
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("🔍 Step 1/4: Searching for content...")
                progress_bar.progress(25)

                try:
                    # Call API
                    api_url = "https://lorf2f330g.execute-api.us-west-2.amazonaws.com/prod/generate-ppt"

                    request_data = {
                        "description": st.session_state.topic,
                        "urls": urls,
                        "slide_count": slide_count
                    }

                    status_text.text("📝 Step 2/4: Processing content...")
                    progress_bar.progress(50)

                    # Add document text if available
                    if st.session_state.document_text:
                        import base64
                        document_text_bytes = st.session_state.document_text.encode('utf-8')
                        document_text_b64 = base64.b64encode(document_text_bytes).decode('utf-8')

                        # Check size
                        text_size_mb = len(document_text_b64) / (1024 * 1024)
                        if text_size_mb > 8:
                            error_msg = f"""
                            ⚠️ **Document too large ({text_size_mb:.2f}MB)**

                            The uploaded document exceeds the 8MB limit.

                            **Please:**
                            - Use a shorter document
                            - Or remove the document and use search only
                            """
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                            st.error(error_msg)
                            st.session_state.waiting_for_urls = False
                            st.session_state.topic = None
                            st.stop()

                        request_data['document_text_b64'] = document_text_b64

                    # Add uploaded file data if available
                    if st.session_state.uploaded_file is not None:
                        import base64

                        st.session_state.uploaded_file.seek(0)
                        file_bytes = st.session_state.uploaded_file.read()
                        file_extension = '.' + st.session_state.uploaded_file.name.split('.')[-1]

                        file_size_mb = len(file_bytes) / (1024 * 1024)

                        if file_size_mb > 3:
                            error_msg = f"⚠️ **Data file too large ({file_size_mb:.1f}MB)**\n\nMaximum allowed: 3MB"
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                            st.error(error_msg)
                            st.session_state.waiting_for_urls = False
                            st.session_state.topic = None
                            st.stop()

                        file_b64 = base64.b64encode(file_bytes).decode('utf-8')

                        request_data['csv_data'] = file_b64
                        request_data['file_extension'] = file_extension

                    status_text.text("🎨 Step 3/4: Generating slides...")
                    progress_bar.progress(75)

                    response = requests.post(
                        api_url,
                        json=request_data,
                        headers={'Content-Type': 'application/json'},
                        timeout=120
                    )

                    status_text.text("✅ Step 4/4: Finalizing presentation...")
                    progress_bar.progress(100)

                    if response.status_code == 200:
                        result = response.json()

                        if 'download_url' in result:
                            info = result.get('pptx_info', {})
                            success_msg = f"✅ **Success! Your presentation is ready with {info.get('slide_count', 'N/A')} slides!**"

                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": success_msg,
                                "download_url": result['download_url'],
                                "pptx_info": info
                            })

                            status_text.empty()
                            progress_bar.empty()

                            st.markdown(success_msg)

                            # Show download section
                            st.markdown("""
                            <div class='success-box'>
                                <h2 style='color: white; margin: 0;'>🎉 Your Presentation is Ready!</h2>
                            </div>
                            """, unsafe_allow_html=True)

                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("📊 Slides", info.get('slide_count', 'N/A'))
                            with col2:
                                st.metric("🖼️ Images", info.get('images_inserted', 0))
                            with col3:
                                size_kb = info.get('size_bytes', 0) / 1024
                                st.metric("💾 Size", f"{size_kb:.0f} KB")
                            with col4:
                                st.markdown("<br>", unsafe_allow_html=True)

                            st.markdown(f"""
                            <a href="{result['download_url']}" target="_blank">
                                <button style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; border: none; border-radius: 25px; padding: 15px 40px; font-size: 1.2em; font-weight: bold; cursor: pointer; width: 100%; margin: 20px 0; box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);'>
                                    📥 Download Your Presentation
                                </button>
                            </a>
                            """, unsafe_allow_html=True)

                        else:
                            error_msg = "❌ No download link received from server"
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                            st.error(error_msg)
                    else:
                        error_msg = f"❌ Server error (Status: {response.status_code})"
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.error(error_msg)

                    # Reset state for new conversation
                    st.session_state.waiting_for_urls = False
                    st.session_state.topic = None
                    st.session_state.current_step = 1

                except requests.Timeout:
                    error_msg = "⏱️ **Request timed out**\n\nThe server took too long to respond. Please try again."
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)
                    st.session_state.waiting_for_urls = False
                    st.session_state.topic = None
                    st.session_state.current_step = 1

                except Exception as e:
                    error_msg = f"❌ **Error occurred**\n\n{str(e)}\n\nPlease try again or contact support."
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)
                    st.session_state.waiting_for_urls = False
                    st.session_state.topic = None
                    st.session_state.current_step = 1

# Footer with better styling
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666; border-top: 2px solid #e0e0e0; margin-top: 50px;'>
    <p><strong>💡 Pro Tip:</strong> Upload documents and data files for even better presentations!</p>
    <p style='font-size: 0.9em; color: #999;'>Made with ❤️ by Hemanth Raju K | Powered by Claude Sonnet 4.5 AI</p>
</div>
""", unsafe_allow_html=True)
