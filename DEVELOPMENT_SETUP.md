# HTH Development Setup Guide

## 🚀 Quick Start

### Prerequisites Check
```bash
# Check Node.js version (should be 16+)
node --version

# Check Python version (should be 3.8+)
python --version

# Check if Git is installed
git --version

# Check if FFmpeg is installed
ffmpeg -version
```

## 🛠️ Environment Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd HTH
```

### 2. Backend Environment
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# If requirements.txt doesn't exist, install manually:
pip install flask flask-cors python-dotenv
```

### 3. Frontend Environment
```bash
cd hth-ui

# Install dependencies
npm install

# Verify installation
npm list --depth=0
```

## 🔧 Configuration Files

### Backend Configuration
Create `backend/.env` file:
```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=104857600
```

### Frontend Configuration
Update `hth-ui/vite.config.js`:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  },
  define: {
    global: 'globalThis',
  }
})
```

## 🚀 Running the Application

### 1. Start Backend Server
```bash
cd backend

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Start Flask server
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 2. Start Frontend Server
```bash
cd hth-ui

# Start development server
npm run dev
```

**Expected Output:**
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://xxx.xxx.xxx.xxx:5173/
```

### 3. Verify Both Servers
- Backend: http://localhost:5000
- Frontend: http://localhost:5173

## 📁 Project Structure Understanding

### Backend Structure
```
backend/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
├── uploads/               # User uploaded files
│   └── .gitkeep          # Keep folder in git
└── subtitles/             # Generated content
    ├── MonsterDubs.mp4    # English video
    ├── interactive_subs.json
    ├── subtitles.srt
    └── index.html
```

### Frontend Structure
```
hth-ui/
├── package.json           # Node.js dependencies
├── vite.config.js         # Vite configuration
├── index.html             # Entry point
├── src/
│   ├── main.jsx          # React entry point
│   ├── App.jsx           # Main app component
│   ├── Home.jsx          # Home page
│   ├── Processing.jsx    # Video processing page
│   ├── TrackedVideoPlayer.jsx # Custom video player
│   ├── index.css         # Global styles
│   └── App.css           # App-specific styles
├── public/
│   ├── videos/           # Multi-language videos
│   ├── transcripts/      # Multi-language transcripts
│   └── vite.svg          # Vite logo
└── transcripts/           # Source transcript files
```

## 🔍 Development Workflow

### 1. Making Changes
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes to files
# Test changes locally

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/new-feature
```

### 2. Testing Changes
```bash
# Backend testing
cd backend
python -m pytest tests/  # If tests exist

# Frontend testing
cd hth-ui
npm test                 # If tests exist
npm run build            # Build check
```

### 3. Hot Reload
- **Backend**: Flask debug mode enables auto-reload
- **Frontend**: Vite provides instant hot reload

## 🐛 Debugging

### Backend Debugging
```python
# Add debug prints
print(f"Debug: {variable}")

# Use Flask debugger
import pdb; pdb.set_trace()

# Check logs
app.logger.info("Info message")
app.logger.error("Error message")
```

### Frontend Debugging
```javascript
// Console logging
console.log('Debug:', variable);
console.error('Error:', error);

// React DevTools
// Install React Developer Tools browser extension

// Debug state changes
useEffect(() => {
  console.log('State changed:', state);
}, [state]);
```

### Network Debugging
```javascript
// Check API calls
fetch('/api/endpoint')
  .then(response => {
    console.log('Response status:', response.status);
    console.log('Response headers:', response.headers);
    return response.json();
  })
  .then(data => console.log('Response data:', data))
  .catch(error => console.error('Fetch error:', error));
```

## 🔧 Common Issues & Solutions

### Backend Issues

#### 1. Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

#### 2. Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. CORS Issues
```python
# Ensure CORS is properly configured
from flask_cors import CORS
CORS(app, origins=["http://localhost:5173"])
```

### Frontend Issues

#### 1. Port Already in Use
```bash
# Kill process on port 5173
npx kill-port 5173
```

#### 2. Node Modules Issues
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 3. Build Issues
```bash
# Clear build cache
npm run build -- --force
```

## 📚 Development Tools

### Recommended VS Code Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "formulahendry.auto-rename-tag",
    "christian-kohler.path-intellisense"
  ]
}
```

### VS Code Settings
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "python.defaultInterpreterPath": "./backend/venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true
}
```

## 🧪 Testing Setup

### Backend Testing
```bash
cd backend

# Install testing dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Frontend Testing
```bash
cd hth-ui

# Install testing dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## 📦 Building for Production

### Backend Production
```bash
cd backend

# Install production dependencies
pip install gunicorn

# Build and run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Production
```bash
cd hth-ui

# Build production version
npm run build

# Preview production build
npm run preview

# Deploy dist/ folder to web server
```

## 🔄 Database Setup (Future)

### SQLite Setup
```bash
cd backend

# Install database dependencies
pip install flask-sqlalchemy

# Initialize database
flask db init
flask db migrate
flask db upgrade
```

### Environment Variables
```env
DATABASE_URL=sqlite:///hth.db
FLASK_APP=app.py
FLASK_ENV=development
```

## 📊 Monitoring & Logging

### Backend Logging
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/hth.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('HTH startup')
```

### Frontend Logging
```javascript
// Create logger utility
const logger = {
  info: (message, data) => {
    if (process.env.NODE_ENV === 'development') {
      console.log(`[INFO] ${message}`, data);
    }
  },
  error: (message, error) => {
    console.error(`[ERROR] ${message}`, error);
  }
};

// Usage
logger.info('User action', { action: 'video_upload', userId: 123 });
```

## 🚀 Deployment Checklist

### Pre-deployment
- [ ] All tests passing
- [ ] Build successful
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files optimized
- [ ] Security headers configured

### Production Environment
```bash
# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=0

# Use production WSGI server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

**Last Updated**: August 2025  
**Version**: 1.0.0  
**Maintainer**: Development Team 