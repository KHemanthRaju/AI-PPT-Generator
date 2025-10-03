import json
from lambda_final import lambda_handler

# Test the Lambda function locally
test_event = {
    'body': json.dumps({
        'description': 'Create a presentation about Amazon Bedrock',
        'urls': ['https://aws.amazon.com/bedrock/']
    })
}

try:
    result = lambda_handler(test_event, None)
    print("Lambda Response:")
    print(json.dumps(json.loads(result['body']), indent=2))
except Exception as e:
    print(f"Error: {e}")