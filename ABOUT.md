# AI PowerPoint Generator

## Overview

The AI PowerPoint Generator is an intelligent presentation creation tool powered by **Claude Sonnet 4.5 AI** from Anthropic. It automatically generates professional, well-structured PowerPoint presentations from various input sources including web content, documents, and data files.

## 🎯 Purpose

This tool is designed to save time and effort in creating professional presentations by:
- Automating content research and extraction
- Generating insightful, concise slide content
- Creating data visualizations from Excel/CSV files
- Converting lengthy documents into presentation-ready slides
- Maintaining professional design standards throughout

## 👥 Target Audience

### Students
- Convert thesis/dissertations into defense presentations
- Create project presentation slides from reports
- Generate presentations from research papers
- Transform group project documents into slides

### Professionals
- Create business presentations from reports
- Convert proposals into pitch decks
- Generate stakeholder presentations quickly
- Transform technical documents into executive summaries

### Researchers
- Create conference presentations from papers
- Generate research overview slides
- Convert findings into presentation format
- Share research insights effectively

## ✨ Key Features

### 1. **AI-Powered Content Generation**
- Uses Claude Sonnet 4.5 for intelligent content synthesis
- Generates insight-based slide titles (not just topic headings)
- Creates concise, impactful bullet points
- Maintains professional 6×6 rule standards

### 2. **Multi-Source Content Extraction**
- **Web Search**: Automatically searches and extracts relevant web content
- **URL Crawling**: Fetches content from provided URLs
- **Document Conversion**: Extracts text from PDF/DOC/DOCX files
- **Link Detection**: Automatically finds and crawls URLs within documents
- **Image Extraction**: Downloads and analyzes relevant images

### 3. **Data Analysis & Visualization**
- Reads Excel/CSV files with automatic structure detection
- Generates professional charts (bar, line, pie)
- Analyzes data trends and generates insights
- Highlights key data points in visualizations
- Handles date columns and complex data types

### 4. **Professional Presentation Standards**
- **6×6 Rule**: Maximum 4 bullets per slide, 6-8 words per bullet
- **Typography**: Calibri 36pt titles, 20pt body text
- **High Contrast**: Dark blue titles, dark gray body text
- **Bullet Points**: Visible bullet symbols (•) on all content slides
- **Clean Design**: Minimal, professional appearance
- **Consistent Formatting**: Same fonts, colors, and alignment throughout

### 5. **Flexible Slide Count**
- Dynamic slide generation (3-15 slides)
- User-configurable via slider
- Automatically includes title and closing slides
- Adapts content to fit requested slide count

## 🏗️ Architecture

### Frontend
- **Framework**: Streamlit (Python web framework)
- **Port**: 8501 (http://localhost:8501)
- **Features**:
  - File upload (Excel, CSV, PDF, DOC, DOCX)
  - Real-time text extraction
  - Base64 encoding for data transmission
  - Continuous chat history within session
  - Download link generation

### Backend
- **Platform**: AWS Lambda (serverless compute)
- **Runtime**: Python 3.9
- **Memory**: 1024 MB
- **Timeout**: 300 seconds (5 minutes)
- **Region**: us-west-2

### AI Engine
- **Model**: Claude Sonnet 4.5
- **Service**: AWS Bedrock
- **Capabilities**:
  - Natural language understanding
  - Content synthesis and summarization
  - Data analysis and insight generation
  - JSON-structured output generation

### Storage
- **Service**: AWS S3
- **Bucket**: ppt-generator-1759467436-803633136603
- **Purpose**: Temporary storage of generated presentations
- **Access**: Pre-signed URLs with expiration

### API Gateway
- **Endpoint**: https://lorf2f330g.execute-api.us-west-2.amazonaws.com/prod/generate-ppt
- **Method**: POST
- **Payload Limit**: 10MB
- **Timeout**: 120 seconds

## 🔧 Technical Stack

### Core Libraries
- **python-pptx**: PowerPoint file generation
- **pandas**: Data processing and analysis
- **matplotlib**: Chart generation
- **PyPDF2**: PDF text extraction
- **python-docx**: Word document text extraction
- **boto3**: AWS SDK for Python
- **streamlit**: Web UI framework
- **requests**: HTTP client for API calls

### AWS Services
- **Lambda**: Serverless compute for presentation generation
- **Bedrock**: AI model hosting (Claude Sonnet 4.5)
- **S3**: Object storage for presentations
- **API Gateway**: RESTful API endpoint
- **CloudWatch**: Logging and monitoring
- **IAM**: Access management

## 📊 Data Flow

1. **User Input** → Streamlit UI
2. **File Upload** → Base64 encoding
3. **API Request** → API Gateway
4. **Lambda Function** → Processing:
   - Document text extraction
   - URL detection and crawling
   - Excel/CSV parsing
   - Chart generation with matplotlib
   - Claude AI content synthesis
   - PowerPoint generation with python-pptx
5. **S3 Upload** → Generated presentation
6. **Pre-signed URL** → User download link
7. **Response** → Streamlit displays download link

## 🎨 Design Principles

### Content Quality
- **One Message Per Slide**: Each slide communicates a single key insight
- **Insight-Based Titles**: Titles state findings, not just topics
- **Concise Bullets**: Short, powerful phrases (6-8 words maximum)
- **Strategic Whitespace**: Proper margins and spacing

### Visual Consistency
- **Typography**: Calibri font family throughout
- **Color Palette**: Professional dark blue and gray
- **Alignment**: Left-aligned for easy reading
- **Hierarchy**: Clear title-body relationship

### Accessibility
- **High Contrast**: Easy to read on any screen
- **Readable Font Sizes**: Never below 16pt
- **Bullet Symbols**: Explicit visual markers
- **Clean Layout**: No visual clutter

## 📈 Performance

### Speed
- **Average Generation Time**: 30-60 seconds
- **Web Search**: ~5 seconds
- **URL Crawling**: ~2-3 seconds per URL
- **Chart Generation**: ~1 second per chart
- **AI Processing**: ~10-15 seconds
- **PowerPoint Generation**: ~5 seconds

### Limits
- **Excel/CSV Files**: 3MB maximum
- **Document Text**: 8MB maximum (base64 encoded)
- **Total Request Payload**: 10MB (API Gateway limit)
- **Lambda Execution**: 300 seconds maximum
- **Concurrent Requests**: No hard limit (Lambda auto-scales)

## 🔒 Security

### Data Privacy
- Files are processed in-memory only
- No permanent storage of user data
- Presentations stored temporarily in S3
- Pre-signed URLs expire after download

### Access Control
- AWS IAM roles for service permissions
- S3 bucket policies for access control
- API Gateway authorization
- No public access to Lambda functions

## 🚀 Deployment

### Local Development
```bash
# Start Streamlit server
streamlit run chatbot_ui.py
```

### Lambda Deployment
```bash
# Package function
zip -j lambda-update.zip lambda_final.py

# Deploy to AWS
aws lambda update-function-code \
  --function-name ppt-generator-backend \
  --zip-file fileb://lambda-update.zip
```

### Dependencies Layer
```bash
# Build Lambda layer with Docker
./build_layer.sh
```

## 📝 Version History

### Latest Version (2026-03-03)
- ✅ PDF/DOC document upload and conversion
- ✅ Automatic URL detection and crawling from documents
- ✅ Base64 encoding for special character handling
- ✅ Simplified UI with reduced information overload
- ✅ Enhanced error handling and user feedback
- ✅ Dynamic slide count selection (3-15 slides)
- ✅ Professional 6×6 rule implementation
- ✅ Bullet symbol visibility fix
- ✅ DateTime serialization fix for Excel files
- ✅ Image insertion counter accuracy fix

### Previous Features
- Excel/CSV data analysis with chart generation
- Web content extraction and image analysis
- Professional typography and design standards
- Continuous chat history within session

## 👨‍💻 Creator

**Hemanth Raju K**
- Master's Student, Arizona State University
- Computer Science (4.0 GPA)
- AWS Certified Solutions Architect
- Full-Stack Developer with AI/ML expertise

### Contact
- GitHub: [KHemanthRaju](https://github.com/KHemanthRaju)
- LinkedIn: [Hemanth Raju Koneti](https://linkedin.com/in/hemanth-raju-koneti)

## 📄 License

This project is created for educational and professional purposes.

## 🙏 Acknowledgments

- **Anthropic**: Claude Sonnet 4.5 AI model
- **AWS**: Cloud infrastructure and services
- **Python Community**: Open-source libraries
- **Streamlit**: Web framework for rapid development

## 📚 Documentation

For detailed feature documentation, see:
- [DOCUMENT_TO_PPT_FEATURE.md](DOCUMENT_TO_PPT_FEATURE.md)
- [PDF_URL_CRAWLING_FEATURE.md](PDF_URL_CRAWLING_FEATURE.md)
- [PROFESSIONAL_STANDARDS.md](PROFESSIONAL_STANDARDS.md)
- [MODERN_6x6_STANDARDS.md](MODERN_6x6_STANDARDS.md)

## 🎯 Future Enhancements

### Planned Features
1. **Persistent Chat History** - Save conversations across sessions
2. **Template Library** - Pre-designed presentation themes
3. **Image Upload** - Custom images from users
4. **Collaborative Editing** - Multi-user presentation editing
5. **Export Formats** - PDF, Google Slides, Keynote
6. **Advanced Analytics** - Usage statistics and insights
7. **API Authentication** - User accounts and API keys
8. **Batch Processing** - Multiple presentations at once
9. **Custom Branding** - Company logos and colors
10. **Version Control** - Track presentation revisions

### Technical Improvements
- **Caching** - Store crawled content for faster regeneration
- **Parallel Processing** - Fetch multiple URLs simultaneously
- **OCR Support** - Extract text from scanned PDFs
- **Table Extraction** - Parse tables from documents
- **Code Highlighting** - Syntax highlighting for technical presentations
- **LaTeX Support** - Mathematical equations in slides

## 📞 Support

For issues, questions, or feature requests:
- Create an issue on GitHub
- Contact the creator directly
- Check documentation files

## 🎉 Get Started

Visit http://localhost:8501 to start creating professional presentations!

1. Upload your files (Excel/PDF/DOC)
2. Type your presentation topic
3. Type "search" to auto-generate
4. Download your presentation

It's that simple! ✨
