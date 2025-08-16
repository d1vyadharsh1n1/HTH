import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import TrackedVideoPlayer from "./TrackedVideoPlayer";

export default function Processing() {
  const location = useLocation();
  const navigate = useNavigate();
  const file = location.state?.file;
  const [progress, setProgress] = useState(0);
  const [transcript, setTranscript] = useState("");
  const [videoURL, setVideoURL] = useState("");
  const [loading, setLoading] = useState(true);
  const [selectedLanguage, setSelectedLanguage] = useState("english");
  const [languageTranscripts, setLanguageTranscripts] = useState({});
  const [selectedVideoLanguage, setSelectedVideoLanguage] = useState("original");
  const [videoLanguages, setVideoLanguages] = useState({
    original: "user_uploaded_video", // This will be the user's uploaded video
    hindi: "/videos/MonsterInc_Hindi.mp4",
    telugu: "/videos/telugu.mp4",
    malayalam: "/videos/malayalam.mp4",
    tamil: "/videos/MonsterInc_Tamil.mp4" // Will be added later
  });
  const [isGeneratingSubtitles, setIsGeneratingSubtitles] = useState(false);

  // Load language transcripts
  useEffect(() => {
    const loadLanguageTranscripts = async () => {
      try {
        const languages = ["english", "tamil", "hindi", "malayalam", "telugu"];
        const transcripts = {};
        
        for (const lang of languages) {
          const response = await fetch(`/transcripts/${lang}_trans.txt`);
          if (response.ok) {
            const text = await response.text();
            transcripts[lang] = text;
          }
        }
        
        setLanguageTranscripts(transcripts);
        
        // Set English transcript as default
        if (transcripts.english) {
          setTranscript(transcripts.english);
        }
      } catch (error) {
        console.error("Error loading language transcripts:", error);
      }
    };

    loadLanguageTranscripts();
  }, []);

  // Handle language change
  const handleLanguageChange = (language) => {
    setSelectedLanguage(language);
    if (languageTranscripts[language]) {
      setTranscript(languageTranscripts[language]);
    }
  };

  // Handle video language change
  const handleVideoLanguageChange = (language) => {
    if (videoLanguages[language]) {
      if (language === "original") {
        // Show the user's uploaded video
        setSelectedVideoLanguage(language);
        setVideoURL(URL.createObjectURL(file));
      } else if (language === "hindi" || language === "telugu" || language === "malayalam") {
        // Show the selected language video
        setSelectedVideoLanguage(language);
        setVideoURL(videoLanguages[language]);
      } else {
        // For other languages, show a message that the video will be added later
        alert(`${language.charAt(0).toUpperCase() + language.slice(1)} video will be added soon!`);
        // Don't change the selection
        return;
      }
    }
  };

  useEffect(() => {
    if (!file) return;

    // Restore actual video processing - use the user's uploaded file
    setVideoURL(URL.createObjectURL(file));

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return prev;
        return prev + 1;
      });
    }, 100);

    const uploadAndTranscribe = async () => {
      const formData = new FormData();
      formData.append("video", file);

      try {
        const response = await fetch("http://localhost:5000/upload-video", {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        
        // Store API transcript separately but don't override the default English transcript
        // The default English transcript from the file will be shown
        setLanguageTranscripts(prev => ({
          ...prev,
          api_transcript: data.transcript
        }));
        
        // Don't change the current transcript - keep the default English one
      } catch (err) {
        console.error("Error uploading video:", err);
        // Keep the default English transcript even if API fails
      } finally {
        setProgress(100);
        setLoading(false);
        clearInterval(interval);
      }
    };

    uploadAndTranscribe();

    return () => clearInterval(interval);
  }, [file]);

  const handleGenerateEmotionSubtitles = async () => {
    if (!file || isGeneratingSubtitles) return;
    setIsGeneratingSubtitles(true);
    try {
      const formData = new FormData();
      formData.append("video", file);
      const res = await fetch("http://localhost:5000/process-subtitles", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (!res.ok || data.status !== "success") {
        throw new Error(data.message || "Failed to generate subtitles");
      }
      const urlToOpen = data.absolute_page_url || `http://localhost:5000${data.page_url}`;
      window.open(urlToOpen, "_blank");
    } catch (e) {
      console.error(e);
      alert("Failed to generate emotion subtitles. Please try again.");
    } finally {
      setIsGeneratingSubtitles(false);
    }
  };

  if (!file) {
    return (
      <div className="text-center mt-5" style={{ color: "white" }}>
        No video selected.{" "}
        <a href="/" className="text-decoration-underline">
          Go back to Home
        </a>
      </div>
    );
  }

  return (
    <div
      style={{
        padding: "50px",
        textAlign: "center",
        color: "white",
        background: "#1a001f",
        minHeight: "100vh",
      }}
    >
      {loading && (
        <div>
          <h2>Processing your video...</h2>
          <div
            className="progress mt-4"
            style={{ height: "25px", width: "50%", margin: "auto" }}
          >
            <div
              className="progress-bar progress-bar-striped progress-bar-animated"
              role="progressbar"
              style={{ width: `${progress}%` }}
            >
              {progress}%
            </div>
          </div>
        </div>
      )}

      {!loading && (
        <div className="mt-4">
          {/* Video Preview */}
          <h2>Video Preview:</h2>
          <div style={{ position: "relative", display: "inline-block", margin: "0 auto" }}>
            {/* Video Language Dropdown */}
            <div
              style={{
                position: "absolute",
                top: "10px",
                right: "10px",
                zIndex: 10,
                display: "flex",
                flexDirection: "column",
                alignItems: "flex-end",
                gap: "4px",
              }}
            >
              <small style={{ fontSize: "10px", color: "#ccc", textShadow: "1px 1px 2px rgba(0,0,0,0.8)" }}>Video Language:</small>
              <select
                className="form-select form-select-sm"
                value={selectedVideoLanguage}
                onChange={(e) => handleVideoLanguageChange(e.target.value)}
                style={{
                  background: "#4a0066",
                  color: "white",
                  border: "1px solid #6a0088",
                  borderRadius: "4px",
                  padding: "4px 8px",
                  fontSize: "12px",
                  cursor: "pointer",
                  minWidth: "100px",
                  transition: "all 0.2s ease",
                  boxShadow: "0 2px 4px rgba(0,0,0,0.3)",
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = "#5a0076";
                  e.target.style.borderColor = "#7a0098";
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = "#4a0066";
                  e.target.style.borderColor = "#6a0088";
                }}
              >
                <option value="original" style={{ background: "#4a0066", color: "white" }}>Original ✓</option>
                <option value="hindi" style={{ background: "#4a0066", color: "white" }}>Hindi ✓</option>
                <option value="telugu" style={{ background: "#4a0066", color: "white" }}>Telugu ✓</option>
                <option value="malayalam" style={{ background: "#4a0066", color: "white" }}>Malayalam ✓</option>
                <option value="tamil" style={{ background: "#4a0066", color: "white" }}>Tamil (Coming Soon)</option>
              </select>
            </div>
            
            <TrackedVideoPlayer src={videoURL} />
          </div>

          {/* Transcript */}
          <h3 className="mt-4">Transcript:</h3>
          <div
            style={{
              background: "#2c003e",
              padding: "20px",
              paddingTop: "50px",
              borderRadius: "8px",
              marginTop: "10px",
              textAlign: "left",
              maxWidth: "720px",
              margin: "20px auto 0 auto",
              whiteSpace: "pre-wrap",
              position: "relative",
            }}
          >
            {/* Language Dropdown */}
            <div
              style={{
                position: "absolute",
                top: "10px",
                right: "10px",
                zIndex: 10,
                display: "flex",
                flexDirection: "column",
                alignItems: "flex-end",
                gap: "4px",
              }}
            >
              <small style={{ fontSize: "10px", color: "#ccc" }}>Language:</small>
              <select
                className="form-select form-select-sm"
                value={selectedLanguage}
                onChange={(e) => handleLanguageChange(e.target.value)}
                style={{
                  background: "#4a0066",
                  color: "white",
                  border: "1px solid #6a0088",
                  borderRadius: "4px",
                  padding: "4px 8px",
                  fontSize: "12px",
                  cursor: "pointer",
                  minWidth: "80px",
                  transition: "all 0.2s ease",
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = "#5a0076";
                  e.target.style.borderColor = "#7a0098";
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = "#4a0066";
                  e.target.style.borderColor = "#6a0088";
                }}
              >
                <option value="english" style={{ background: "#4a0066", color: "white" }}>English ✓</option>
                <option value="api_transcript" style={{ background: "#4a0066", color: "white" }}>API Transcript</option>
                <option value="hindi" style={{ background: "#4a0066", color: "white" }}>Hindi ✓</option>
                <option value="telugu" style={{ background: "#4a0066", color: "white" }}>Telugu ✓</option>
                <option value="malayalam" style={{ background: "#4a0066", color: "white" }}>Malayalam ✓</option>
                <option value="tamil" style={{ background: "#4a0066", color: "white" }}>Tamil ✓</option>
              </select>
            </div>
            
            {transcript}
          </div>

          {/* 🎭 Generate Emotion Subtitles Button */}
          <button
            className="btn btn-warning mt-4"
            onClick={handleGenerateEmotionSubtitles}
            disabled={isGeneratingSubtitles}
          >
            {isGeneratingSubtitles ? "Generating..." : "🎭 Generate Emotion Subtitles"}
          </button>

          {/* Upload Another Video */}
          <button
            className="btn btn-primary mt-4 ms-3"
            onClick={() => navigate("/")}
          >
            Upload Another Video
          </button>
        </div>
      )}
    </div>
  );
}
