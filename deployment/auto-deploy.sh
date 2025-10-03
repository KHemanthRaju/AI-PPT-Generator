#!/bin/bash

set -e

echo "🚀 PowerPoint Generator - Automated Deployment"
echo "=============================================="

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first."
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run: aws configure"
    exit 1
fi

echo "✅ AWS CLI configured"

# Set variables
STACK_NAME="ppt-generator-stack"
REGION="us-west-2"
BUCKET_NAME="ppt-generator-$(date +%s)"

echo "📋 Deployment Configuration:"
echo "   Stack Name: $STACK_NAME"
echo "   Region: $REGION"
echo "   S3 Bucket: $BUCKET_NAME"
echo ""

# Step 1: Check Bedrock models
echo "🔍 Checking Bedrock model access..."
aws bedrock list-foundation-models --region $REGION --by-provider anthropic --query 'modelSummaries[?contains(modelId, `claude`)].modelId' --output text > /tmp/claude_models.txt

if grep -q "claude" /tmp/claude_models.txt; then
    echo "✅ Claude models available"
else
    echo "❌ No Claude models found. Please enable model access in Bedrock console:"
    echo "   https://console.aws.amazon.com/bedrock/"
    echo "   Go to Model Access → Enable Claude models"
    exit 1
fi

# Step 2: Create Lambda layer
echo "📦 Creating Lambda layer..."
mkdir -p python
pip install firecrawl-py python-pptx -t python --platform manylinux2014_x86_64 --only-binary=:all: -q
zip -r layer.zip python > /dev/null
rm -rf python
echo "✅ Lambda layer created"

# Step 3: Deploy CloudFormation
echo "☁️  Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file cloudformation-template.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides BucketName=$BUCKET_NAME \
    --capabilities CAPABILITY_IAM \
    --region $REGION \
    --no-cli-pager

echo "✅ CloudFormation deployed"

# Step 4: Update Lambda code
echo "🔧 Updating Lambda function code..."
zip -j lambda-code.zip deploy_aws_lambda.py > /dev/null
aws lambda update-function-code \
    --function-name ppt-generator-backend \
    --zip-file fileb://lambda-code.zip \
    --region $REGION \
    --no-cli-pager > /dev/null

echo "✅ Lambda code updated"

# Step 5: Get outputs
echo "📊 Getting deployment outputs..."
API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
    --output text)

S3_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' \
    --output text)

# Step 6: Update frontend
echo "🎨 Updating frontend configuration..."
python3 -c "
import re
with open('frontend_chatbot.py', 'r') as f:
    content = f.read()
content = re.sub(r'http://localhost:8000/generate-ppt', '$API_ENDPOINT', content)
with open('frontend_chatbot.py', 'w') as f:
    f.write(content)
print('Frontend updated with API endpoint')
"

# Cleanup
rm -f layer.zip lambda-code.zip /tmp/claude_models.txt

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo "======================="
echo "API Endpoint: $API_ENDPOINT"
echo "S3 Bucket: $S3_BUCKET"
echo ""
echo "🚀 Next Steps:"
echo "1. Run frontend: streamlit run frontend_chatbot.py"
echo "2. Test with: 'Create a 5-slide presentation about AI trends'"
echo ""
echo "📝 Note: Make sure Bedrock model access is enabled for Claude models"