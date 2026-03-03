# PDF URL Crawling Feature

## Overview
The AI PPT Generator now automatically detects and crawls URLs found in uploaded PDF/DOC documents. When you upload a document containing hyperlinks (GitHub profiles, LinkedIn profiles, project websites, etc.), the system will:

1. **Extract URLs** from the document text
2. **Crawl those websites** to fetch additional content
3. **Extract images** from the crawled websites
4. **Combine all content** (document text + website content + images) into the presentation

## Use Case
This feature is particularly useful for:
- **Resumes/CVs with links**: GitHub profiles, LinkedIn, portfolio websites
- **Reports with references**: Links to external resources, documentation
- **Project documents**: Links to live demos, GitHub repos, documentation
- **Research papers**: Links to datasets, supplementary materials, related work

## How It Works

### Step-by-Step Process

#### 1. **Upload PDF with Links**
When you upload a PDF in the sidebar, the system:
- Extracts all text from the PDF
- Scans the text for URLs using regex pattern: `https?://[...]`
- Displays detected URLs count in the UI

#### 2. **Automatic URL Detection**
The system finds URLs in formats like:
- `https://github.com/username`
- `http://example.com/page`
- URLs embedded in text or paragraphs

#### 3. **Website Crawling**
For each detected URL, the Lambda function:
- Sends HTTP request to fetch the webpage
- Extracts text content using HTML parsing
- Extracts images from the webpage
- Downloads and encodes images for presentation

#### 4. **Content Combination**
All content sources are merged:
- Document text (from your PDF)
- Website text (from crawled URLs)
- Images (from crawled websites)
- Charts (if Excel/CSV is also uploaded)

#### 5. **AI Processing**
Claude Sonnet 4.5 analyzes all combined content and creates professional slides.

## Technical Implementation

### Frontend (chatbot_ui.py)

#### URL Detection in UI
```python
# Check for URLs in the text after extraction
url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
found_urls = re.findall(url_pattern, text)
unique_urls = list(set([url.rstrip('.,;:!?)') for url in found_urls]))

if unique_urls:
    st.info(f"📊 Extracted {word_count:,} words from document\n🔗 Found {len(unique_urls)} link(s) - will crawl these websites too!")
```

### Backend (lambda_final.py)

#### URL Extraction and Crawling
```python
# Extract URLs from document text
url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+(?:[^\s.,;!?)\]]|(?<=\w)[.,;!?)])'
found_urls = re.findall(url_pattern, document_text)

# Clean up URLs (remove trailing punctuation)
cleaned_urls = []
for url in found_urls:
    url = url.rstrip('.,;:!?)')
    if url and url not in cleaned_urls:
        cleaned_urls.append(url)

# Add to main URL list for crawling
if not urls:
    urls = []
urls.extend(cleaned_urls)
```

#### Website Content Extraction
The existing URL crawling logic handles:
- HTTP request with User-Agent header
- HTML parsing and text extraction
- Image detection and download
- Base64 encoding for images
- Error handling for failed requests

## Example Workflow

### Scenario: Resume with GitHub Profile

**Input:**
- PDF: "Hemanth_Raju_Resume.pdf"
- Contains: `https://github.com/KHemanthRaju`
- Topic: "Professional profile presentation"

**Process:**
1. Upload PDF → System extracts text
2. System detects: `https://github.com/KHemanthRaju`
3. UI shows: "🔗 Found 1 link(s) - will crawl these websites too!"
4. Lambda crawls GitHub profile page
5. Extracts: Bio, pinned repos, contributions, profile image
6. Combines: Resume text + GitHub profile content
7. Claude creates slides with:
   - Professional background (from resume)
   - GitHub projects (from profile)
   - Skills and contributions
   - Profile image

**Output:**
Professional presentation with comprehensive information from both resume and GitHub profile!

## Benefits

### ✅ Comprehensive Content
- Automatically enriches presentations with online profiles
- No need to manually copy-paste from websites
- Always uses latest online information

### ✅ Time Saving
- One upload instead of providing multiple sources
- Automatic detection and crawling
- No manual URL entry required

### ✅ Up-to-Date Information
- Fetches current website content
- Real-time GitHub/LinkedIn profiles
- Latest project information

### ✅ Professional Completeness
- Combines written document with online presence
- Includes images from websites
- Creates holistic professional profile

## Supported URL Formats

### ✅ Fully Supported
- `https://github.com/username`
- `https://linkedin.com/in/username`
- `https://example.com/portfolio`
- `http://website.com/page`
- URLs in plain text paragraphs
- Multiple URLs per document

### ⚠️ Limitations
- URLs must be in standard format (http:// or https://)
- Password-protected pages are skipped
- Very large pages may timeout (15s limit)
- Some websites may block automated requests

## Error Handling

### Graceful Failures
If a URL fails to crawl:
- Error is logged but doesn't stop generation
- Other URLs continue to process
- Document text is still used
- Presentation is generated with available content

### Common Issues
1. **URL blocked by website**: Skipped, other content used
2. **Timeout (>15s)**: Skipped, other content used
3. **Invalid URL format**: Ignored during extraction
4. **404 Not Found**: Logged, generation continues

## Testing

### Test Your PDF
1. Upload a PDF containing URLs
2. Check sidebar for detection message
3. Generate presentation
4. Verify combined content in slides

### Example Test Files
- Resume with GitHub/LinkedIn links
- Project report with demo website links
- Research paper with reference URLs
- Portfolio document with project links

## Configuration

### URL Pattern Regex
```python
# Detects URLs with common formats
url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+(?:[^\s.,;!?)\]]|(?<=\w)[.,;!?)])'
```

### Timeout Settings
- URL crawling timeout: **15 seconds per URL**
- Total Lambda timeout: **300 seconds**

### Limits
- No limit on number of URLs detected
- Each URL independently crawled
- Combined content sent to Claude for analysis

## User Experience

### Before Feature
```
User: *uploads resume with GitHub link*
User: "Also check https://github.com/KHemanthRaju"
System: *generates from resume + manually provided URL*
```

### After Feature
```
User: *uploads resume with GitHub link*
System: "🔗 Found 1 link(s) - will crawl these websites too!"
User: Type "search"
System: *automatically crawls GitHub, generates comprehensive presentation*
```

**Result:** One step instead of two, automatic detection, no manual URL entry!

## Deployment Status

### ✅ Deployed
- **Lambda Function**: Updated with URL extraction logic
- **Streamlit UI**: Shows detected URL count
- **API Endpoint**: Processes document URLs automatically
- **Server**: http://localhost:8501

### Version
- Feature added: 2026-03-03
- Lambda function: ppt-generator-backend (latest)
- Status: **LIVE AND READY TO USE**

## Future Enhancements

### Planned
1. **URL Validation**: Check if URL is accessible before crawling
2. **Custom User-Agent**: Better compatibility with websites
3. **Parallel Crawling**: Fetch multiple URLs simultaneously
4. **URL Preview**: Show extracted URLs before generating
5. **Selective Crawling**: Let user choose which URLs to include

### Advanced Features
- Handle redirects intelligently
- Extract more structured data (tables, code blocks)
- Support authentication for private repositories
- Cache crawled content for faster regeneration

## Summary

The PDF URL Crawling feature transforms how users create presentations from documents. By automatically detecting and crawling links found in PDFs, the system creates more comprehensive, up-to-date, and professional presentations without requiring manual URL entry or copy-pasting from websites.

**Key Takeaway**: Upload a resume with your GitHub/LinkedIn links, and the system automatically creates a complete professional profile presentation by combining your resume with your online presence!
