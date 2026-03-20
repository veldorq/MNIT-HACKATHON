#!/bin/bash
# NewsGuard Full Stack Deployment Script
# Deploys: Backend to Heroku + Frontend to Vercel

set -e

echo "🚀 NewsGuard Deployment Script"
echo "=============================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v heroku &> /dev/null; then
    echo -e "${YELLOW}⚠️  Heroku CLI not found. Install from: https://devcenter.heroku.com/articles/heroku-cli${NC}"
    exit 1
fi

if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}ℹ️  Installing Vercel CLI...${NC}"
    npm install -g vercel
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"
echo ""

# Step 1: Build Frontend
echo -e "${BLUE}Step 1: Building frontend...${NC}"
cd frontend
npm install
npm run build
echo -e "${GREEN}✓ Frontend built (dist/ ready)${NC}"
echo ""

# Step 2: Deploy Backend
echo -e "${BLUE}Step 2: Deploying backend to Heroku...${NC}"
cd ../backend

# Check if already deployed
if heroku apps:list | grep -q "newsguard-api"; then
    echo -e "${YELLOW}App 'newsguard-api' already exists. Skipping creation.${NC}"
else
    echo "Creating Heroku app..."
    heroku create newsguard-api
fi

echo "Setting environment variables..."
heroku config:set FLASK_ENV=production
heroku config:set FRONTEND_ORIGIN=https://newsguard-frontend.vercel.app  
heroku config:set MODEL_VARIANT=hybrid

echo "Deploying code..."
git push heroku main 2>/dev/null || git push heroku HEAD:main

BACKEND_URL="https://newsguard-api.herokuapp.com"
echo -e "${GREEN}✓ Backend deployed${NC}"
echo -e "Backend URL: ${BACKEND_URL}"
echo ""

# Step 3: Deploy Frontend
echo -e "${BLUE}Step 3: Deploying frontend to Vercel...${NC}"
cd ../frontend

# Deploy with environment variable
vercel --prod --env VITE_API_URL=$BACKEND_URL

FRONTEND_URL="https://newsguard-frontend.vercel.app"
echo -e "${GREEN}✓ Frontend deployed${NC}"
echo -e "Frontend URL: ${FRONTEND_URL}"
echo ""

# Step 4: Verify Connection
echo -e "${BLUE}Step 4: Testing connection...${NC}"
sleep 2

echo "Testing backend..."
if curl -s "${BACKEND_URL}/api/models" > /dev/null; then
    echo -e "${GREEN}✓ Backend is responding${NC}"
else
    echo -e "${YELLOW}⚠️  Backend not responding yet (wait a moment for Heroku to start)${NC}"
fi

echo ""
echo -e "${GREEN}=============================="
echo "🎉 Deployment Complete!${NC}"
echo "=============================="
echo ""
echo "📊 Your URLs:"
echo "  Frontend: ${FRONTEND_URL}"
echo "  Backend:  ${BACKEND_URL}"
echo ""
echo "✅ Next steps:"
echo "  1. Open ${FRONTEND_URL} in your browser"
echo "  2. Try analyzing some text"
echo "  3. Share the frontend URL with judges/team"
echo ""
echo "📖 For more info, see DEPLOYMENT.md"
echo ""
