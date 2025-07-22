#!/bin/bash

# AutoShield DApp Deployment Setup Script
echo "🚀 Setting up AutoShield DApp for deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
# Dependencies
node_modules/
*/node_modules/

# Production builds
.next/
dist/
build/

# Environment variables
.env
.env.local
.env.production
*.env

# Logs
*.log
logs/

# OS generated files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env/
.venv/

# AI Services
*.pkl
*.joblib
*.model

# Temporary files
*.tmp
*.temp
EOF
fi

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add your files to git: git add ."
echo "2. Commit your changes: git commit -m 'Initial commit'"
echo "3. Create a GitHub repository and push your code"
echo "4. Follow the deployment guide in DEPLOYMENT_GUIDE.md"
echo ""
echo "🔗 Useful links:"
echo "- Vercel: https://vercel.com"
echo "- Render: https://render.com"
echo "- GitHub: https://github.com"
