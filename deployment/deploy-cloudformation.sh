#!/bin/bash

STACK_NAME="ppt-generator-stack"
BUCKET_NAME="ppt-generator-$(date +%s)"
REGION="us-west-2"

echo "Deploying PPT Generator Backend with CloudFormation..."
echo "⚠️  IMPORTANT: Make sure Bedrock model access is enabled first!"
echo "   See bedrock-setup.md for instructions"
echo ""
read -p "Have you enabled Claude 3.5 Sonnet v2 in Bedrock? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please enable Bedrock model access first. See bedrock-setup.md"
    exit 1
fi

# Step 1: Create Lambda layer ZIP
echo "Creating Lambda layer..."
./create_lambda_layer.sh

# Step 2: Create temporary S3 bucket for deployment artifacts
TEMP_BUCKET="cf-deploy-$(date +%s)"
aws s3 mb s3://$TEMP_BUCKET

# Step 3: Upload layer to temp bucket
aws s3 cp layer.zip s3://$TEMP_BUCKET/

# Step 4: Deploy CloudFormation stack
aws cloudformation deploy \
    --template-file cloudformation-template.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides BucketName=$BUCKET_NAME \
    --capabilities CAPABILITY_IAM \
    --region $REGION

# Step 5: Get stack outputs
API_ENDPOINT=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`ApiEndpoint`].OutputValue' \
    --output text)

S3_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' \
    --output text)

# Step 6: Update Lambda function code
echo "Updating Lambda function code..."
zip -j lambda-code.zip deploy_aws_lambda.py
aws lambda update-function-code \
    --function-name ppt-generator-backend \
    --zip-file fileb://lambda-code.zip

# Step 7: Copy layer to actual S3 bucket
aws s3 cp layer.zip s3://$S3_BUCKET/

# Cleanup
aws s3 rb s3://$TEMP_BUCKET --force
rm -f layer.zip lambda-code.zip

echo "Deployment complete!"
echo "API Endpoint: $API_ENDPOINT"
echo "S3 Bucket: $S3_BUCKET"
echo ""
echo "Update your frontend with:"
echo "API_URL = '$API_ENDPOINT'"