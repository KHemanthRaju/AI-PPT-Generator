#!/bin/bash

echo "Deploying backend to AWS Lambda..."

# Create deployment package
mkdir -p lambda-package
cp deploy_aws_lambda.py lambda-package/lambda_function.py

# Create ZIP file
cd lambda-package
zip -r ../lambda-deployment.zip .
cd ..

# Deploy to Lambda (requires AWS CLI configured)
aws lambda create-function \
    --function-name ppt-generator-backend \
    --runtime python3.9 \
    --role arn:aws:iam::YOUR-ACCOUNT:role/lambda-execution-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://lambda-deployment.zip \
    --timeout 300 \
    --memory-size 512

echo "Lambda function created. Don't forget to:"
echo "1. Add Lambda layer with dependencies"
echo "2. Set S3_BUCKET_NAME environment variable"
echo "3. Create API Gateway endpoint"

# Cleanup
rm -rf lambda-package lambda-deployment.zip