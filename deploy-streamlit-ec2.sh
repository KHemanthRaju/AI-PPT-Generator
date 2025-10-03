#!/bin/bash
# Deploy Streamlit to EC2

# 1. Launch EC2 instance (t2.micro for free tier)
# 2. SSH into instance
# 3. Run this script

sudo yum update -y
sudo yum install -y python3 python3-pip git

# Clone your repo
git clone https://github.com/YOUR_USERNAME/ai-ppt-generator.git
cd ai-ppt-generator

# Install dependencies
pip3 install -r requirements.txt

# Install PM2 for process management
sudo npm install -g pm2

# Create PM2 ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'streamlit-app',
    script: 'streamlit',
    args: 'run chatbot_frontend.py --server.port 8501 --server.address 0.0.0.0',
    interpreter: 'python3'
  }]
}
EOF

# Start with PM2
pm2 start ecosystem.config.js
pm2 startup
pm2 save

echo "Streamlit running on http://YOUR_EC2_IP:8501"