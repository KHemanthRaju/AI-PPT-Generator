# Security Guidelines

## 🔐 API Key Management

### ❌ Never commit API keys to Git:
- Firecrawl API keys
- AWS credentials
- Any secret tokens

### ✅ Use environment variables:
```bash
# Copy template
cp .env.example .env

# Add your keys
FIRECRAWL_API_KEY=your_actual_key_here
AWS_ACCESS_KEY_ID=your_aws_key
```

### ✅ For production:
- Use AWS Secrets Manager
- Use IAM roles instead of access keys
- Enable MFA on AWS accounts

## 🛡️ Best Practices

1. **Rotate keys regularly**
2. **Use least privilege IAM policies**
3. **Monitor API usage**
4. **Enable CloudTrail logging**

## 🚨 If keys are exposed:
1. Immediately revoke the compromised keys
2. Generate new keys
3. Update all applications
4. Review access logs