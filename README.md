# Amazon Bedrock PowerPoint Generator

An AI-powered system that automatically creates PowerPoint presentations by searching the web, generating slides, and getting the downloadable link.

## Features

- **Web Search**: Uses Firecrawl to gather information from the internet
- **PowerPoint Generation**: Creates professional PPTX files with multiple slides
- **Interactive Frontend**: Streamlit-based chat interface
- **Real-time Tracing**: Shows AI agent decision-making process

## Technologies Used

### Backend
- **Amazon Bedrock** - AI agent orchestration and LLM integration
- **AWS Lambda** - Serverless compute for backend functions
- **Amazon S3** - File storage for generated PowerPoint presentations
- **Amazon SNS** - Email notification service
- **Amazon API Gateway** - REST API endpoints
- **Python 3.9+** - Backend programming language

### Frontend
- **Streamlit** - Interactive web interface
- **React.js** - Alternative frontend (Amplify deployment)
- **AWS Amplify** - Frontend hosting and deployment

### Libraries & APIs
- **python-pptx** - PowerPoint file generation
- **boto3** - AWS SDK for Python
- **Firecrawl API** - Web scraping and content extraction
- **requests** - HTTP client library

### Development & Deployment
- **Docker** - Containerization (Dev Container support)
- **AWS CloudFormation** - Infrastructure as Code
- **Git** - Version control
- **Bash** - Deployment scripts

## Architecture

The system uses Amazon Bedrock Agents with three Lambda functions:
1. `search-web` - Performs web searches using Firecrawl
2. `create-pptx` - Generates PowerPoint files and uploads to S3

## Quick Start

1. **Setup AWS Resources**
   - Follow instructions in `setup_instructions.md`
   - Deploy Lambda functions using provided code
   - Configure Bedrock agent with action groups

2. **Create Lambda Layer**
   ```bash
   ./create_lambda_layer.sh
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Frontend**
   ```bash
   streamlit run chatbot_frontend.py
   ```

## Usage Examples

```
"Research the latest AI trends and create a PowerPoint"
"Create slides about Amazon Bedrock features"
"Research quantum computing and make a presentation"
```

## Files

- `lambda_search_web.py` - Web search Lambda function
- `lambda_create_pptx.py` - PowerPoint creation Lambda function  
- `chatbot_frontend.py` - Streamlit web interface
- `create_lambda_layer.sh` - Script to create Lambda layer
- `setup_instructions.md` - Detailed setup guide

## Requirements

- AWS Account with Bedrock access
- Firecrawl API key (set in environment variables)
- Python 3.9+
- Streamlit, boto3, python-pptx

## Cost Optimization

The system uses serverless architecture to minimize costs:
- Lambda functions only run when triggered
- S3 storage for generated files
- SNS for email notifications
- Bedrock pay-per-use pricing

## Security Notes

- Store API keys in environment variables
- Use IAM roles with minimal required permissions
- Enable MFA on AWS root account
- Consider using AWS Secrets Manager for production
