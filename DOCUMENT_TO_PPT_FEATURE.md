# Document to PPT Conversion Feature

## Overview
The AI PPT Generator now supports converting PDF and DOC/DOCX documents directly into professional presentations. This feature is designed for students, researchers, and professionals who need to convert written reports, thesis, dissertations, and project documents into presentation slides.

## Use Cases

### 1. **Academic Use Cases**
- **Thesis/Dissertation Presentations**: Convert your written thesis into a presentation for your defense
- **Research Papers**: Transform research papers into conference presentation slides
- **Lab Reports**: Convert detailed lab reports into summary presentations
- **Literature Reviews**: Create presentation slides from written literature review documents

### 2. **Professional Use Cases**
- **Project Reports**: Convert project documentation into stakeholder presentation slides
- **Business Reports**: Transform written business reports into executive presentations
- **Proposals**: Convert proposal documents into pitch presentations
- **White Papers**: Create presentation slides from technical white papers

### 3. **Student Use Cases**
- **Group Project Reports**: Convert written group project reports into presentation slides
- **Essay Presentations**: Transform essays into visual presentations for class
- **Case Study Analysis**: Convert written case studies into presentation format
- **Book Reports**: Create presentation slides from book report documents

## How It Works

### Frontend (Streamlit UI)
1. **Document Upload Widget**: Located in the sidebar, accepts PDF, DOC, and DOCX files
2. **Text Extraction**:
   - **PDF**: Uses PyPDF2 library to extract text from all pages
   - **DOCX**: Uses python-docx library to extract text from all paragraphs
3. **Word Count Display**: Shows the number of words extracted from the document
4. **Content Integration**: Extracted text is sent to the Lambda backend along with the topic description

### Backend (AWS Lambda)
1. **Parameter Extraction**: Lambda function receives `document_text` parameter from the request
2. **Content Processing**: Document text is added to `extracted_content` list
3. **AI Analysis**: Claude Sonnet 4.5 analyzes the document text and creates presentation structure
4. **Slide Generation**: Professional slides are generated following the 6×6 rule and modern presentation standards

## Technical Implementation

### Libraries Used
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **io.BytesIO**: In-memory file handling

### Code Flow

#### Frontend (chatbot_ui.py)
```python
# 1. Text Extraction Functions
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n\n"
    return text.strip()

def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    doc = Document(io.BytesIO(docx_file.read()))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()

# 2. Document Upload Widget
uploaded_document = st.file_uploader(
    "Upload PDF, DOC, or DOCX document",
    type=['pdf', 'doc', 'docx'],
    help="Upload reports, thesis, dissertations, or project documents to convert to presentation"
)

# 3. Send to API
request_data = {
    "description": st.session_state.topic,
    "urls": urls,
    "slide_count": slide_count,
    "document_text": st.session_state.document_text  # Extracted text
}
```

#### Backend (lambda_final.py)
```python
# 1. Extract document_text parameter
document_text = body.get('document_text', None)

# 2. Add to extracted content
if document_text:
    extracted_content.append({
        'source': 'uploaded_document',
        'content': document_text
    })

# 3. Claude processes the content and generates slides
```

## Features

### ✅ Supported Formats
- **PDF** (.pdf) - All versions
- **DOC/DOCX** (.doc, .docx) - Microsoft Word documents

### ✅ Professional Standards
All document-to-PPT conversions follow:
- **6×6 Rule**: Max 4 bullets per slide, 6-8 words per bullet
- **Typography**: Calibri 36pt titles, 20pt body text
- **Layout**: 3-zone layout (headline → visual → supporting points)
- **Bullet Symbols**: Visible bullet points (•) on all content slides
- **Clean Design**: Minimal, professional appearance

### ✅ AI Processing
- **Intelligent Summarization**: Claude extracts key points from lengthy documents
- **Structure Detection**: Identifies main topics and subtopics
- **Insight Generation**: Creates insight-based slide titles (not just topic titles)
- **Content Prioritization**: Focuses on most important information

## User Experience

### Step-by-Step Process
1. **Upload Document**: Click "Upload PDF, DOC, or DOCX document" in sidebar
2. **View Extraction**: See word count and extraction confirmation
3. **Provide Topic**: Tell the chatbot what presentation you want
4. **Choose Content Source**:
   - Option 1: Type "search" for web search + document
   - Option 2: Provide URLs for specific sources + document
   - Option 3: Just use document (type "search" and document will be used)
5. **Generate**: AI processes document and creates presentation
6. **Download**: Get professional PPT file ready to present

### Example Conversation
```
You: Create a presentation about my research project

Bot: Great! What URLs should I use?

You: search
[Note: User has uploaded "Research_Paper.pdf" in sidebar]

Bot: Perfect! I'll automatically search the web for information
     about your research project and create your presentation.
     📄 Including content from Research_Paper.pdf...

Bot: ✨ Success! Your presentation is ready!
     Source: 🔍 Auto-searched the web, 📄 Converted Research_Paper.pdf to presentation
```

## Benefits

### For Students
- ✅ Save time converting reports to presentations
- ✅ Maintain consistency between written and presented work
- ✅ Professional formatting without manual effort
- ✅ Focus on content, not slide design

### For Researchers
- ✅ Quickly create conference presentations from papers
- ✅ Summarize lengthy research documents effectively
- ✅ Maintain academic presentation standards
- ✅ Adapt content for different audiences

### For Professionals
- ✅ Convert reports to stakeholder presentations
- ✅ Create executive summaries automatically
- ✅ Maintain brand consistency with professional design
- ✅ Rapid turnaround for urgent presentations

## Limitations

### Current Limitations
- **Text Only**: Images and tables from documents are not extracted (yet)
- **Formatting**: Complex formatting (colors, fonts) is not preserved
- **Large Files**: Very large documents may take longer to process
- **Scanned PDFs**: OCR is not supported; only text-based PDFs work

### Workarounds
- **Images**: Upload document + provide URLs with relevant images
- **Data Tables**: Use Excel/CSV upload feature for data with charts
- **Scanned PDFs**: Convert to text-based PDF first using OCR tools

## Future Enhancements

### Planned Features
1. **Image Extraction**: Extract images and tables from documents
2. **OCR Support**: Handle scanned PDFs with optical character recognition
3. **Format Preservation**: Maintain heading hierarchy and formatting
4. **Multi-Document**: Combine multiple documents into one presentation
5. **Template Matching**: Detect document type and apply appropriate template

## Testing

### Test Files Included
The following test files can be used:
- **PDF**: "Edson E+I TEMPLATE Executive Summary.pdf"
- **Excel**: Project-Management-Sample-Data.xlsx (for comparison)

### Test Scenarios
1. **Simple PDF**: Upload a 2-3 page PDF, request 6 slides
2. **Long Document**: Upload 10+ page thesis, request 10 slides
3. **Combined**: Upload PDF + Excel, provide URLs
4. **DOCX**: Upload Word document with headings

## Deployment Status

### ✅ Deployed Components
- **Frontend**: Streamlit UI with document upload widget
- **Text Extraction**: PyPDF2 and python-docx libraries installed
- **Backend**: Lambda function updated to handle document_text
- **Integration**: Complete end-to-end flow tested

### Server Status
- **Streamlit UI**: http://localhost:8501
- **Lambda Function**: ppt-generator-backend (updated)
- **API Endpoint**: https://lorf2f330g.execute-api.us-west-2.amazonaws.com/prod/generate-ppt

## Summary

The Document-to-PPT feature addresses a critical need for students and professionals who need to convert written documents into presentations. By combining AI-powered text analysis with professional presentation standards, the system creates high-quality slides that effectively communicate the key points from lengthy documents.

**Key Takeaway**: Students no longer need to manually extract content from their thesis, reports, or dissertations—they can simply upload the document and let AI create a professional presentation automatically!
