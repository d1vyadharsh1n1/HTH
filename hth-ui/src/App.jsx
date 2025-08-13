import { useEffect, useState } from "react";

export default function App() {
  const [typedText, setTypedText] = useState("");
  const fullText = "AI-Powered Voiceover & Localization";

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
            LinguaLive
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <a className="nav-link" href="#features">
                  Features
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#pricing">
                  Pricing
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#contact">
                  Contact
                </a>
              </li>
            </ul>
          </div>
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
            className="btn btn-lg me-3 hero-btn"
            style={{ backgroundColor: "#8e24aa", color: "white" }}
          >
            🚀 Get Started Free
          </button>
          <button className="btn btn-outline-light btn-lg hero-btn">
            🎥 Book a Demo
          </button>
        </div>
      </header>

      {/* Features Section */}
      <section
        id="features"
        className="py-5"
        style={{ backgroundColor: "#1a001f", color: "white" }}
      >
        <div className="container text-center">
          <h2 className="fw-bold mb-5" style={{ color: "#d8b4ff" }}>
            Why Choose LinguaLive?
          </h2>
          <div className="row g-4">
            {[
              {
                icon: "🌍",
                title: "Cultural Nuances",
                desc: "Go beyond literal translation with AI-powered idiom and context adaptation.",
              },
              {
                icon: "🎙",
                title: "Multi-Format Output",
                desc: "Generate subtitles, scripts, and voiceovers from a single source file.",
              },
              {
                icon: "⚡",
                title: "Real-Time Sync",
                desc: "Translate & dub live webinars, streams, and events instantly.",
              },
            ].map((feature, i) => (
              <div className="col-md-4" key={i}>
                <div className="feature-card p-4 rounded shadow-sm h-100">
                  <h4 className="fw-bold">
                    {feature.icon} {feature.title}
                  </h4>
                  <p>{feature.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer
        className="text-center py-4"
        style={{ backgroundColor: "#0d001a", color: "#b39ddb" }}
      >
        <p className="mb-0">
          &copy; {new Date().getFullYear()} LinguaLive. All Rights Reserved.
        </p>
      </footer>
    </>
  );
}
