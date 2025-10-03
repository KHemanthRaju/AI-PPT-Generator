import streamlit as st
import requests
import json
from create_pptx_local import create_pptx_from_slides

st.title("AI PowerPoint Generator")
st.write("Enter a topic and URLs to create a PowerPoint presentation")

# Input fields
topic = st.text_input("Topic/Description", placeholder="Create a presentation about AI trends")
urls_text = st.text_area("URLs (one per line)", placeholder="https://example.com\nhttps://another-site.com")

if st.button("Generate PowerPoint"):
    if topic:
        # Parse URLs
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        # Prepare request data
        request_data = {
            "description": topic,
            "urls": urls
        }
        
        with st.spinner("Generating PowerPoint..."):
            try:
                # Call your deployed Lambda function
                lambda_url = "https://lorf2f330g.execute-api.us-west-2.amazonaws.com/prod/generate-ppt"
                
                response = requests.post(
                    lambda_url,
                    json=request_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    with st.expander("Debug: API Response"):
                        st.json(result)
                    
                    if 'download_url' in result:
                        st.success("PowerPoint created successfully!")
                        st.markdown(f"### [📥 Download PowerPoint]({result['download_url']})")
                    else:
                        st.warning("Creating PPTX locally...")
                        if 'slides' in result:
                            try:
                                pptx_file = create_pptx_from_slides(result['slides'])
                                with open(pptx_file, 'rb') as f:
                                    st.download_button(
                                        label="📥 Download PowerPoint",
                                        data=f.read(),
                                        file_name=f"presentation_{topic.replace(' ', '_')}.pptx",
                                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                    )
                                import os
                                os.unlink(pptx_file)
                                st.success("PowerPoint created locally!")
                            except Exception as e:
                                st.error(f"Local PPTX creation failed: {e}")
                        
                    if 'slides' in result:
                        st.subheader("Generated Slides:")
                        for i, slide in enumerate(result['slides']['slides'], 1):
                            st.write(f"**Slide {i}: {slide['title']}**")
                            for bullet in slide['content']:
                                st.write(f"• {bullet}")
                            st.write("---")
                else:
                    st.error(f"Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                st.error(traceback.format_exc())
    else:
        st.warning("Please enter a topic")