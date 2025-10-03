# Backend Deployment Options

## Option 1: AWS Lambda (Serverless)

### Steps:
1. **Create Lambda Layer**
   ```bash
   ./create_lambda_layer.sh
   ```

2. **Create Lambda Function**
   - Runtime: Python 3.9
   - Code: Upload `deploy_aws_lambda.py`
   - Layer: Add the created layer
   - Environment variables:
     - `S3_BUCKET_NAME=your-bucket-name`
   - IAM Role: Add S3FullAccess and BedrockFullAccess

3. **Create API Gateway**
   - Create REST API
   - Create POST method `/generate-ppt`
   - Integration: Lambda Function
   - Enable CORS

4. **Update Frontend**
   ```python
   # In frontend_chatbot.py, replace localhost with API Gateway URL
   response = requests.post('https://your-api-id.execute-api.region.amazonaws.com/prod/generate-ppt')
   ```

## Option 2: Docker Container

### Local Docker:
```bash
# Build image
docker build -t ppt-backend .

# Run container
docker run -p 8000:8000 -e S3_BUCKET_NAME=your-bucket ppt-backend
```

### AWS ECS/Fargate:
```bash
# Push to ECR
aws ecr create-repository --repository-name ppt-backend
docker tag ppt-backend:latest your-account.dkr.ecr.region.amazonaws.com/ppt-backend:latest
docker push your-account.dkr.ecr.region.amazonaws.com/ppt-backend:latest

# Deploy to ECS Fargate
# Use AWS Console or CLI to create ECS service
```

## Option 3: AWS App Runner

### Steps:
1. Push code to GitHub
2. Create App Runner service
3. Connect to GitHub repository
4. Set environment variables:
   - `S3_BUCKET_NAME=your-bucket`
5. App Runner will auto-deploy

## Option 4: Local Development

### Run locally:
```bash
# Install dependencies
pip install -r requirements_new.txt

# Set environment variable
export S3_BUCKET_NAME=your-bucket-name

# Run backend
python backend_api.py

# Run frontend (in another terminal)
streamlit run frontend_chatbot.py
```

## Recommended: AWS Lambda + API Gateway

**Pros:**
- Serverless (no server management)
- Pay per request
- Auto-scaling
- Built-in monitoring

**Setup Time:** 15 minutes
**Cost:** ~$0.01 per 1000 requests