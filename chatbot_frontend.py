import streamlit as st
import requests
import json
import os
from create_pptx_local import create_pptx_from_slides

st.title("🤖 AI PowerPoint Generator")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Create a presentation about AI trends with these URLs: https://example.com"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Extract topic, URLs, and slide count from prompt
    lines = prompt.split('\n')
    topic = lines[0]
    urls = [line.strip() for line in lines[1:] if line.strip().startswith('http')]
    
    # If no URLs in separate lines, look for URLs in the main text
    if not urls:
        import re
        urls = re.findall(r'https?://[^\s]+', prompt)
    
    # Extract slide count (default 6)
    import re
    slide_match = re.search(r'(\d+)\s*slides?', prompt.lower())
    slide_count = int(slide_match.group(1)) if slide_match else 6
    
    with st.chat_message("assistant"):
        with st.spinner("Generating PowerPoint..."):
            try:
                # Call API
                response = requests.post(
                    os.environ.get('API_URL', 'https://lorf2f330g.execute-api.us-west-2.amazonaws.com/prod/generate-ppt'),
                    json={"description": topic, "urls": urls, "slide_count": slide_count},
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if 'download_url' in result:
                        st.markdown(f"✅ **PowerPoint created successfully!**\n\n[📥 Download PowerPoint]({result['download_url']})")
                        response_text = f"I've created your PowerPoint presentation! [Download it here]({result['download_url']})"
                    else:
                        # Create locally as fallback
                        if 'slides' in result:
                            pptx_file = create_pptx_from_slides(result['slides'])
                            with open(pptx_file, 'rb') as f:
                                st.download_button(
                                    label="📥 Download PowerPoint",
                                    data=f.read(),
                                    file_name=f"presentation.pptx",
                                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                )
                            import os
                            os.unlink(pptx_file)
                            response_text = "I've created your PowerPoint presentation! Click the download button above."
                        else:
                            response_text = "Sorry, I couldn't create the presentation. Please try again."
                    
                    # Show slide preview
                    if 'slides' in result:
                        st.markdown("**📋 Slide Preview:**")
                        for i, slide in enumerate(result['slides']['slides'], 1):
                            st.markdown(f"**{i}. {slide['title']}**")
                            for bullet in slide['content']:
                                st.markdown(f"• {bullet}")
                else:
                    response_text = f"Error: {response.text}"
                    st.error(response_text)
                    
            except Exception as e:
                response_text = f"Error: {str(e)}"
                st.error(response_text)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})