import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

export default function Home() {
  const [typedText, setTypedText] = useState("");
  const fullText = "AI-Powered Voiceover & Localization";
  const navigate = useNavigate();

  // Typing animation
  useEffect(() => {
    let index = 0;
    const typing = setInterval(() => {
      if (index < fullText.length) {
        setTypedText(fullText.slice(0, index + 1));
        index++;
      } else {
        clearInterval(typing);
      }
    }, 80);
    return () => clearInterval(typing);
  }, []);

  const handleUploadClick = () => {
    document.getElementById("videoInput").click();
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    // Navigate to processing page with file
    navigate("/processing", { state: { file } });
  };

  return (
    <>
      {/* Navbar */}
      <nav
        className="navbar navbar-expand-lg navbar-dark fixed-top shadow"
        style={{ backgroundColor: "#1a001f" }}
      >
        <div className="container">
          <a
            className="navbar-brand fw-bold fs-3"
            style={{ color: "#d8b4ff" }}
            href="#"
          >
            @Lang
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <header
        style={{
          background: "linear-gradient(135deg, #2c003e, #000000)",
          color: "white",
          minHeight: "100vh",
          paddingTop: "70px",
        }}
        className="d-flex flex-column justify-content-center align-items-center text-center"
      >
        <h1
          className="display-3 fw-bold mb-3"
          style={{ color: "#d8b4ff", minHeight: "80px" }}
        >
          {typedText}
        </h1>
        <p
          className="lead mb-4"
          style={{ maxWidth: "700px", color: "#d1c4e9" }}
        >
          Break language barriers with real-time translation, dubbing, and
          cultural adaptation — now smarter and faster.
        </p>
        <div>
          <button
            className="btn btn-lg hero-btn"
            style={{ backgroundColor: "#8e24aa", color: "white" }}
            onClick={handleUploadClick}
          >
            📤 Upload Video
          </button>
          <input
            type="file"
            id="videoInput"
            accept="video/*"
            style={{ display: "none" }}
            onChange={handleFileChange}
          />
        </div>
      </header>
      {/* Features Section */}
      <section
        className="py-5"
        style={{ backgroundColor: "#1a001f", textAlign: "center" }}
      >
        <div className="container">
          <h2 className="display-5 fw-bold mb-4" style={{ color: "#d8b4ff" }}>
            Our Features
          </h2>
          <p className="mb-5" style={{ fontSize: "1.2rem", color: "#e0c3ff" }}>
            Making content localization seamless, engaging, and culturally
            accurate.
          </p>

          <div className="row justify-content-center g-4">
            {/* Feature 1 */}
            <div className="col-sm-6 col-md-3">
              <div
                className="card h-100 text-center shadow-sm border-0"
                style={{
                  background: "linear-gradient(135deg, #8e24aa, #4a0072)",
                  color: "white",
                  transition: "transform 0.3s, box-shadow 0.3s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-10px)";
                  e.currentTarget.style.boxShadow =
                    "0 10px 30px rgba(0,0,0,0.3)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow =
                    "0 4px 15px rgba(0,0,0,0.1)";
                }}
              >
                <div className="card-body">
                  <i className="bi bi-file-earmark-text-fill fs-1 mb-3"></i>
                  <h5 className="card-title fw-bold">AI-Powered Subtitles</h5>
                  <p className="card-text">
                    Generate accurate, multilingual subtitles with cultural
                    context preserved.
                  </p>
                </div>
              </div>
            </div>

            {/* Feature 2 */}
            <div className="col-sm-6 col-md-3">
              <div
                className="card h-100 text-center shadow-sm border-0"
                style={{
                  background: "linear-gradient(135deg, #6a1b9a, #1a001f)",
                  color: "white",
                  transition: "transform 0.3s, box-shadow 0.3s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-10px)";
                  e.currentTarget.style.boxShadow =
                    "0 10px 30px rgba(0,0,0,0.3)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow =
                    "0 4px 15px rgba(0,0,0,0.1)";
                }}
              >
                <div className="card-body">
                  <i className="bi bi-mic-fill fs-1 mb-3"></i>
                  <h5 className="card-title fw-bold">Voiceover Localization</h5>
                  <p className="card-text">
                    Convert content into natural, localized voiceovers using AI
                    speech synthesis.
                  </p>
                </div>
              </div>
            </div>

            {/* Feature 3 */}
            <div className="col-sm-6 col-md-3">
              <div
                className="card h-100 text-center shadow-sm border-0"
                style={{
                  background: "linear-gradient(135deg, #9c27b0, #4a0072)",
                  color: "white",
                  transition: "transform 0.3s, box-shadow 0.3s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-10px)";
                  e.currentTarget.style.boxShadow =
                    "0 10px 30px rgba(0,0,0,0.3)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow =
                    "0 4px 15px rgba(0,0,0,0.1)";
                }}
              >
                <div className="card-body">
                  <i className="bi bi-emoji-smile-fill fs-1 mb-3"></i>
                  <h5 className="card-title fw-bold">
                    Emotion & Tone Matching
                  </h5>
                  <p className="card-text">
                    Retains the emotional tone of your content in all
                    translations and voiceovers.
                  </p>
                </div>
              </div>
            </div>

            {/* Feature 4 */}
            <div className="col-sm-6 col-md-3">
              <div
                className="card h-100 text-center shadow-sm border-0"
                style={{
                  background: "linear-gradient(135deg, #7b1fa2, #1a001f)",
                  color: "white",
                  transition: "transform 0.3s, box-shadow 0.3s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "translateY(-10px)";
                  e.currentTarget.style.boxShadow =
                    "0 10px 30px rgba(0,0,0,0.3)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "translateY(0)";
                  e.currentTarget.style.boxShadow =
                    "0 4px 15px rgba(0,0,0,0.1)";
                }}
              >
                <div className="card-body">
                  <i className="bi bi-plug-fill fs-1 mb-3"></i>
                  <h5 className="card-title fw-bold">Quick Integration</h5>
                  <p className="card-text">
                    Seamlessly integrates with your platforms, websites, and
                    apps for instant localization.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
