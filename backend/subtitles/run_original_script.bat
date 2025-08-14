@echo off
echo ========================================
echo Running Original Working Script
echo ========================================
echo.

echo This will run your original burn_word_subs.py script
echo that you said works perfectly.
echo.

echo Step 1: Running transcript generation...
python burn_word_subs.py

echo.
echo Step 2: If successful, the script will generate:
echo - subtitles.srt (SRT file with emotions)
echo - MonsterDubs.mp4 (Video with burned subtitles)
echo - interactive_subs.json (NEW: JSON for web app)
echo.

echo Step 3: Starting web server...
python start_server.py

echo.
echo ========================================
echo Process Complete!
echo ========================================
echo.
echo If successful:
echo - Your browser will open to http://localhost:8000
echo - The interactive subtitles will use REAL transcript data
echo - You can click words for definitions and see emotions
echo.
echo If you see errors, check:
echo 1. Python is installed and working
echo 2. Required packages: transformers torch requests ffmpeg-python
echo 3. Your AssemblyAI API key is valid
echo 4. MonsterInc.mp4 file exists
echo.
pause 