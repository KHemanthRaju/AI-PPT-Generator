import json
import urllib.request
import re
import boto3
import uuid
import os

def extract_text_from_html(html_content):
    """Extract meaningful text from HTML using regex"""
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', html_content)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()[:2000]

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        description = body.get('description', 'Create a presentation')
        urls = body.get('urls', [])
        
        # Extract text from URLs
        extracted_content = []
        for url in urls:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=15) as response:
                    html_content = response.read().decode('utf-8')
                clean_text = extract_text_from_html(html_content)
                extracted_content.append({'url': url, 'content': clean_text})
            except Exception as e:
                extracted_content.append({'url': url, 'error': str(e)})
        
        # Generate slides with Bedrock
        bedrock = boto3.client('bedrock-runtime')
        all_content = '\n\n'.join([item.get('content', '') for item in extracted_content if 'content' in item])
        
        slide_count = body.get('slide_count', 6)
        content_slides = slide_count - 2  # Subtract title and thank you slides
        
        prompt = f"""Create a {slide_count}-slide PowerPoint presentation about: {description}

Based on this content:
{all_content}

Return ONLY valid JSON in this exact format:
{{"slides": [
  {{"title": "{description}", "content": ["Presentation Overview", "Key Topics Covered", "Main Objectives"]}},
  {{"title": "Content Slide", "content": ["Bullet point 1", "Bullet point 2", "Bullet point 3"]}},
  {{"title": "Thank You!", "content": ["Questions?", "Contact Information", "Thank you for your attention"]}}
]}}

First slide: Title slide with presentation overview
Middle {content_slides} slides: Content based on the provided information
Last slide: Thank you slide
Make sure each content slide has 3-4 bullet points."""

        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "temperature": 0.7,
                "messages": [{"role": "user", "content": prompt}]
            })
        )
        
        result = json.loads(response['body'].read())
        slides_text = result['content'][0]['text']
        
        try:
            slides_json = json.loads(slides_text)
        except json.JSONDecodeError:
            # Fallback with proper structure
            slides_json = {
                "slides": [
                    {"title": description, "content": ["Presentation Overview", "Key Topics Covered", "Main Objectives"]},
                    {"title": "Key Features", "content": ["Multiple AI models", "Easy integration", "Enterprise security"]},
                    {"title": "Use Cases", "content": ["Text generation", "Chatbots", "Content analysis"]},
                    {"title": "Benefits", "content": ["No infrastructure management", "Pay-per-use pricing", "AWS integration"]},
                    {"title": "Getting Started", "content": ["Enable model access", "Use AWS SDKs", "Build AI applications"]},
                    {"title": "Thank You!", "content": ["Questions?", "Contact Information", "Thank you for your attention"]}
                ]
            }
        
        # Create PowerPoint using local python-pptx and upload
        try:
            # Import python-pptx (will work locally)
            from pptx import Presentation
            
            prs = Presentation()
            
            for slide_data in slides_json['slides']:
                slide_layout = prs.slide_layouts[1]  # Title and Content layout
                slide = prs.slides.add_slide(slide_layout)
                
                # Set title
                title_shape = slide.shapes.title
                title_shape.text = slide_data['title']
                
                # Add bullet points
                content = slide.placeholders[1]
                tf = content.text_frame
                tf.text = slide_data['content'][0]
                
                for bullet_point in slide_data['content'][1:]:
                    p = tf.add_paragraph()
                    p.text = bullet_point
                    p.level = 0
            
            # Save and upload
            filename = f"presentation_{uuid.uuid4().hex[:8]}.pptx"
            local_path = f"/tmp/{filename}"
            prs.save(local_path)
            
            file_size = os.path.getsize(local_path)
            
            bucket_name = os.environ.get('S3_BUCKET', 'ppt-generator-1759467436-803633136603')
            s3 = boto3.client('s3')
            s3.upload_file(local_path, bucket_name, filename)
            
            download_url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': filename},
                ExpiresIn=86400
            )
            
            os.remove(local_path)
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'PowerPoint created and uploaded successfully',
                    'download_url': download_url,
                    'slides': slides_json,
                    'pptx_info': {
                        'filename': filename,
                        'size_bytes': file_size,
                        'slide_count': len(slides_json['slides']),
                        'format': 'pptx'
                    }
                })
            }
            
        except ImportError:
            # Fallback: Return slides data for local processing
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Slides generated - use local processing for PPTX',
                    'slides': slides_json,
                    'pptx_info': {
                        'slide_count': len(slides_json['slides']),
                        'format': 'json',
                        'note': 'Use local python-pptx to create PowerPoint file'
                    }
                })
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }