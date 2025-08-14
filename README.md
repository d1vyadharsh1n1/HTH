# HTH (Hear The Heart) - Video Processing & Multi-Language Transcript System

## 📖 Project Overview

HTH is a comprehensive video processing application that provides multi-language transcript support, emotion-based subtitle generation, and interactive video playback. The system consists of a React frontend and a Python Flask backend, designed to handle video uploads, transcription, and multi-language content delivery.

## 🏗️ Architecture

```
HTH/
├── backend/                 # Python Flask Backend
│   ├── app.py              # Main Flask application
│   ├── uploads/            # User uploaded videos
│   └── subtitles/          # Generated subtitles and videos
├── hth-ui/                 # React Frontend
│   ├── src/                # React source code
│   ├── public/             # Static assets
│   └── transcripts/        # Multi-language transcript files
```

## 🚀 Features

### 🎥 Video Processing
- **Video Upload**: Drag & drop or file selection interface
- **Multi-Format Support**: MP4, MP3, and other common video formats
- **Progress Tracking**: Real-time upload and processing progress bar
- **Video Preview**: Interactive video player with tracking capabilities

### 🌍 Multi-Language Support
- **Transcript Languages**: English, Tamil, Hindi, Malayalam, Telugu
- **Dynamic Switching**: Real-time language switching for transcripts
- **Video Languages**: Multi-language video versions (Hindi available, others coming soon)
- **Localized Content**: Region-specific transcript and video content

### 🎭 Emotion Subtitles
- **AI-Generated Subtitles**: Emotion-aware subtitle generation
- **Interactive Playback**: Clickable subtitle segments
- **Timing Synchronization**: Precise subtitle timing with video
- **Web Interface**: Dedicated subtitle viewing platform

## 🛠️ Technology Stack

### Frontend
- **React 18**: Modern React with hooks and functional components
- **Vite**: Fast build tool and development server
- **CSS3**: Custom styling with responsive design
- **HTML5 Video**: Advanced video playback capabilities

### Backend
- **Python Flask**: Lightweight web framework
- **FFmpeg**: Video processing and manipulation
- **Speech Recognition**: Audio transcription capabilities
- **RESTful API**: Clean API design for frontend communication

## 📋 Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **FFmpeg** (for video processing)
- **Git** (for version control)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd HTH
```

### 2. Backend Setup
```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup
```bash
cd hth-ui

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The frontend will run on `http://localhost:5173`

## 🔧 Configuration

### Backend Configuration
- **Port**: Default 5000 (configurable in `app.py`)
- **Upload Directory**: `backend/uploads/`
- **Subtitle Directory**: `backend/subtitles/`
- **CORS**: Configured for local development

### Frontend Configuration
- **Port**: Default 5173 (configurable in `vite.config.js`)
- **API Endpoint**: `http://localhost:5000`
- **Video Sources**: Configured for local development

## 📁 Project Structure

### Backend Structure
```
backend/
├── app.py                  # Main Flask application
├── uploads/                # User uploaded videos
│   ├── MonsterInc.mp3
│   ├── MonsterInc.mp4
│   └── Photosynthesis-*.mp4
└── subtitles/              # Generated content
    ├── MonsterDubs.mp4     # English dubbed video
    ├── interactive_subs.json
    ├── subtitles.srt
    └── index.html          # Subtitle viewer
```

### Frontend Structure
```
hth-ui/
├── src/
│   ├── App.jsx            # Main application component
│   ├── Home.jsx           # Home page with video upload
│   ├── Processing.jsx     # Video processing page
│   ├── TrackedVideoPlayer.jsx # Custom video player
│   └── assets/            # Static assets
├── public/
│   ├── videos/            # Multi-language videos
│   │   └── MonsterInc_Hindi.mp4
│   └── transcripts/       # Multi-language transcripts
│       ├── hindi_trans.txt
│       ├── tamil_trans.txt
│       ├── malayalam_trans.txt
│       └── telugu_trans.txt
└── transcripts/            # Source transcript files
```

## 🎯 Usage Guide

### 1. Video Upload
1. Navigate to the home page
2. Drag & drop a video file or click to select
3. Wait for the processing progress bar
4. Video will be automatically processed and displayed

### 2. Language Switching
1. **Transcript Language**: Use the dropdown in the top-right of the transcript box
2. **Video Language**: Use the dropdown in the top-right of the video preview
3. Select from available languages (English, Hindi, Tamil, Malayalam, Telugu)

### 3. Emotion Subtitles
1. Click the "🎭 Generate Emotion Subtitles" button
2. Wait for processing completion
3. A new tab will open with the interactive subtitle viewer
4. Click on subtitle segments to jump to specific video timestamps

### 4. Video Navigation
- Use the custom video player controls
- Click on transcript segments to jump to specific parts
- Navigate through different language versions

## 🔌 API Endpoints

### Backend API
- `POST /upload-video`: Upload and process video files
- `GET /generate_subtitles`: Generate emotion-based subtitles
- `GET /subtitles/<filename>`: Serve subtitle files and videos

### Frontend Routes
- `/`: Home page with video upload
- `/processing`: Video processing and display page
- `/subtitles`: Subtitle viewing interface (external)

## 🌐 Multi-Language Support

### Available Languages
| Language | Transcript | Video | Status |
|----------|------------|-------|---------|
| English  | ✅         | ✅     | Available |
| Hindi    | ✅         | ✅     | Available |
| Tamil    | ✅         | ⏳     | Coming Soon |
| Malayalam| ✅         | ⏳     | Coming Soon |
| Telugu   | ✅         | ⏳     | Coming Soon |

### Adding New Languages
1. **Transcripts**: Add `{language}_trans.txt` to `hth-ui/transcripts/`
2. **Videos**: Add `MonsterInc_{Language}.mp4` to `hth-ui/public/videos/`
3. **Update Code**: Add language to `videoLanguages` state in `Processing.jsx`

## 🎨 Customization

### Styling
- **Color Scheme**: Dark theme with purple accents
- **Responsive Design**: Mobile-friendly interface
- **Custom Components**: Tailored video player and UI elements

### Video Processing
- **Supported Formats**: MP4, MP3, AVI, MOV
- **Quality Settings**: Configurable in backend
- **Processing Pipeline**: Customizable video processing steps

## 🐛 Troubleshooting

### Common Issues
1. **Backend Connection Error**: Ensure Flask server is running on port 5000
2. **Video Upload Fails**: Check file format and size limits
3. **Language Switching Not Working**: Verify transcript files exist in correct locations
4. **Subtitle Generation Fails**: Check backend subtitle generation service

### Debug Mode
- **Frontend**: Check browser console for React errors
- **Backend**: Check Flask logs for Python errors
- **Network**: Verify API endpoints are accessible

## 🔮 Future Enhancements

### Planned Features
- [ ] Real-time video processing
- [ ] Advanced subtitle customization
- [ ] Multi-user support
- [ ] Cloud storage integration
- [ ] Mobile app development
- [ ] Additional language support

### Technical Improvements
- [ ] WebSocket integration for real-time updates
- [ ] Database integration for user management
- [ ] Caching layer for improved performance
- [ ] Automated testing suite
- [ ] CI/CD pipeline

## 📝 Contributing

### Development Guidelines
1. Follow React best practices
2. Use functional components with hooks
3. Maintain consistent code style
4. Add proper error handling
5. Include documentation for new features

### Code Structure
- **Components**: Single responsibility principle
- **State Management**: Use React hooks appropriately
- **API Calls**: Centralized in service functions
- **Styling**: Inline styles for component-specific styling

## 📄 License

This project is proprietary software. All rights reserved.

## 👥 Team

- **Frontend Development**: React/JavaScript
- **Backend Development**: Python/Flask
- **Video Processing**: FFmpeg integration
- **UI/UX Design**: Custom component design

## 📞 Support

For technical support or feature requests, please contact the development team.

---

**Last Updated**: August 2025
**Version**: 1.0.0
**Status**: Active Development 