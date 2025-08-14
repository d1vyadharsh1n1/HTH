import { useState, useRef, useEffect } from "react";

export default function TrackedVideoPlayer({ src, onHighlightUpdate }) {
  const videoRef = useRef(null);
  const [replays, setReplays] = useState([]); // store rewind timestamps
  const [highlights, setHighlights] = useState([]); // timeline markers

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    let lastTime = 0;

    const handleTimeUpdate = () => {
      const currentTime = video.currentTime;

      // Detect rewinds >1 sec
      if (currentTime < lastTime - 1) {
        setReplays((prev) => {
          const updated = [...prev, currentTime];
          if (onHighlightUpdate) onHighlightUpdate(updated);
          return updated;
        });
        setHighlights((prev) => [...prev, currentTime]);
      }

      lastTime = currentTime;
    };

    const handleEnded = () => {
      // If highlights are too short, highlight full video
      if (
        highlights.length === 0 ||
        (highlights.length === 1 && video.duration - highlights[0] < 1)
      ) {
        setHighlights([0, video.duration]);
        setReplays([0, video.duration]);
        if (onHighlightUpdate) onHighlightUpdate([0, video.duration]);
      }
    };

    video.addEventListener("timeupdate", handleTimeUpdate);
    video.addEventListener("ended", handleEnded);

    return () => {
      video.removeEventListener("timeupdate", handleTimeUpdate);
      video.removeEventListener("ended", handleEnded);
    };
  }, [highlights, onHighlightUpdate]);

  const renderHighlights = () => {
    if (!videoRef.current) return null;
    const duration = videoRef.current.duration;
    if (!duration) return null;

    return highlights.map((time, index) => {
      let left = 0;
      let width = 4; // default width

      if (time === 0 && highlights[1] === duration) {
        // full highlight
        left = 0;
        width = "100%";
      } else {
        left = `${(time / duration) * 100}%`;
        width = `${Math.max((1 / duration) * 100, 0.5)}%`; // at least 0.5%
      }

      return (
        <div
          key={index}
          style={{
            position: "absolute",
            left,
            width,
            height: "100%",
            backgroundColor: "#d8b4ff",
            borderRadius: "2px",
          }}
        ></div>
      );
    });
  };

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        maxWidth: "800px",
        margin: "0 auto",
      }}
    >
      <video
        ref={videoRef}
        src={src}
        controls
        style={{ width: "100%", borderRadius: "10px" }}
      ></video>

      {/* Timeline highlights */}
      {videoRef.current && (
        <div
          style={{
            position: "absolute",
            bottom: "35px",
            left: 0,
            width: "100%",
            height: "5px",
            backgroundColor: "#555",
            borderRadius: "2px",
          }}
        >
          {renderHighlights()}
        </div>
      )}
    </div>
  );
}
