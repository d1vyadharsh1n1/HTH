# 🎬 Interactive Subtitles for Monster Inc.

An AI-powered interactive subtitle system that makes movie watching an educational experience!

## ✨ Features

- **🎨 Emotion-Colorized Subtitles**: Words are colored based on detected emotions
- **📚 Clickable Definitions**: Click any word to see its definition and usage example
- **😊 Emotion Indicators**: Emoji indicators show the emotional context
- **🔄 Toggle Modes**: Switch between emotion colors and normal subtitles
- **⏯️ Video Synchronization**: Subtitles sync perfectly with video playback

## 🚀 Quick Start

### Option 1: Simple Start (Recommended)
1. **Start the server**:
   ```bash
   python start_server.py
   ```
2. **Your browser will open automatically** to `http://localhost:8000`
3. **Enjoy the interactive experience!**

### Option 2: Manual Start
1. Open `index.html` in your web browser
2. The interactive subtitles will load automatically

## 🎯 How to Use

1. **Play the video** - The Monster Inc clip will start playing
2. **Watch the subtitles** - Words appear in different colors based on emotions:
   - 😊 **Yellow** = Joy
   - 😔 **Blue** = Sadness  
   - 😡 **Red** = Anger
   - 😨 **Purple** = Fear
   - 😲 **Orange** = Surprise
   - ❤️ **Pink** = Love
   - 😐 **White** = Neutral

3. **Click any word** - A modal will appear with:
   - Word definition
   - Usage example
   - Emotion classification

4. **Toggle modes** - Use the button to switch between emotion colors and normal subtitles

## 📁 Project Structure

```
HTH_copy/
├── index.html              # Main web page
├── script.js               # Interactive functionality
├── styles.css              # Styling and animations
├── MonsterInc.mp4          # Video file
├── interactive_subs.json   # Subtitle data (generated)
├── generate_mock_subs.py   # Mock data generator
├── start_server.py         # Local server
└── README.md              # This file
```

## 🔧 Technical Details

### Frontend Technologies
- **HTML5 Video Player** with custom subtitle overlay
- **JavaScript** for real-time subtitle rendering and interactions
- **CSS3** for animations and emotion-based color coding

### Data Structure
Each subtitle entry contains:
```json
{
  "start": 0,           // Start time in milliseconds
  "end": 800,           // End time in milliseconds  
  "text": "Hey,",       // The word or phrase
  "emotion": "joy",     // Detected emotion
  "definition": "...",  // Word definition
  "example": "..."      // Usage example
}
```

## 🎨 Customization

### Adding New Emotions
1. Edit `script.js` - Add new emotion colors in the CSS classes
2. Edit `styles.css` - Add corresponding color styles
3. Update the emoji mapping in `script.js`

### Using Different Videos
1. Replace `MonsterInc.mp4` with your video
2. Generate new subtitle data using `generate_mock_subs.py`
3. Update the video source in `index.html`

## 🐛 Troubleshooting

**Video doesn't play?**
- Make sure the video file is in the same directory
- Check that your browser supports MP4 playback

**Subtitles don't appear?**
- Verify `interactive_subs.json` exists and is valid JSON
- Check browser console for JavaScript errors

**Server won't start?**
- Make sure port 8000 is available
- Try a different port by editing `start_server.py`

## 🎉 Enjoy Your Interactive Movie Experience!

This project demonstrates how AI can enhance entertainment by making it educational. Each word becomes a learning opportunity, and emotions add context to the dialogue.

---

*Built with ❤️ for interactive learning* 