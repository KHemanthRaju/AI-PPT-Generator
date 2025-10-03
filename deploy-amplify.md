# Deploy to AWS Amplify

## Steps:

1. **Push to GitHub**
   ```bash
   cd amplify-frontend
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ai-ppt-generator.git
   git push -u origin main
   ```

2. **Deploy on Amplify**
   - Go to AWS Amplify Console
   - Click "New app" → "Host web app"
   - Connect GitHub repository
   - Select branch: `main`
   - Build settings: Auto-detected (uses amplify.yml)
   - Click "Save and deploy"

3. **Environment Variables** (if needed)
   - In Amplify Console → App settings → Environment variables
   - Add: `REACT_APP_API_URL` = `https://lorf2f330g.execute-api.us-west-2.amazonaws.com/prod/generate-ppt`

## Features:
- ✅ Chatbot interface
- ✅ PowerPoint generation
- ✅ Download links
- ✅ Slide previews
- ✅ Responsive design
- ✅ Auto-deployment from GitHub

## URL:
Your app will be available at: `https://main.XXXXXX.amplifyapp.com`