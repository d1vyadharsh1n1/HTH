document.addEventListener("DOMContentLoaded", () => {
    const videoPlayer = document.getElementById("videoPlayer");
    const subtitleOverlay = document.getElementById("subtitle-overlay");
    const modal = document.getElementById("modal");
    const modalText = document.getElementById("modal-text");
    const closeButton = document.querySelector(".close-button");
    const toggleModeButton = document.getElementById("toggle-mode");

    let subtitles = [];
    let isEmotionMode = true;

    const emojiMap = {
        'joy': '😊',
        'sadness': '😔',
        'anger': '😡',
        'fear': '😨',
        'surprise': '😲',
        'love': '❤️',
        'neutral': '😐'
    };

    // --- Fetch and load subtitle data ---
    fetch("interactive_subs.json")
        .then(response => response.json())
        .then(data => {
            subtitles = data;
        })
        .catch(error => console.error('Error loading subtitles:', error));

    // --- Video Time Update Listener ---
    videoPlayer.addEventListener("timeupdate", () => {
        const currentTime = videoPlayer.currentTime * 1000; // Convert to ms
        const words = subtitles.filter(word => 
            currentTime >= word.start && currentTime <= word.end
        );
        
        subtitleOverlay.innerHTML = ''; // Clear previous subtitles
        if (words.length > 0) {
            // Group words into lines based on punctuation
            const lines = [];
            let currentLine = [];
            words.forEach(word => {
                currentLine.push(word);
                if (word.text.endsWith('.') || word.text.endsWith('!') || word.text.endsWith('?')) {
                    lines.push(currentLine);
                    currentLine = [];
                }
            });
            if (currentLine.length > 0) {
                lines.push(currentLine);
            }

            // Display each line
            lines.forEach(lineWords => {
                const lineDiv = document.createElement('div');
                lineWords.forEach(word => {
                    const wordSpan = document.createElement('span');
                    let emotion = word.emotion;
                    
                    // Toggle mode
                    let colorClass = isEmotionMode ? `emotion-${emotion}` : 'emotion-neutral';
                    wordSpan.classList.add('subtitle-word', colorClass);
                    
                    wordSpan.textContent = word.text;
                    wordSpan.dataset.definition = word.definition;
                    wordSpan.dataset.example = word.example;
                    wordSpan.dataset.emotion = emotion;

                    wordSpan.addEventListener('click', handleWordClick);
                    lineDiv.appendChild(wordSpan);
                });

                // Add emotion emoji
                if (isEmotionMode && lineWords.length > 0) {
                    const emojiSpan = document.createElement('span');
                    emojiSpan.textContent = emojiMap[lineWords[0].emotion];
                    emojiSpan.classList.add('subtitle-word');
                    emojiSpan.style.marginRight = '10px';
                    emojiSpan.addEventListener('click', () => {
                        showModal(`Emotion: ${lineWords[0].emotion.toUpperCase()}`);
                    });
                    lineDiv.prepend(emojiSpan);
                }

                subtitleOverlay.appendChild(lineDiv);
            });
        }
    });

    // --- Event Handlers ---
    const handleWordClick = (e) => {
        const word = e.target;
        const definition = word.dataset.definition;
        const example = word.dataset.example;
        const emotion = word.dataset.emotion;
        
        let modalContent = `
            <h2>${word.textContent.toUpperCase()}</h2>
            <p><strong>Definition:</strong> ${definition}</p>
            <p><strong>Example:</strong> ${example}</p>
            <p><strong>Emotion:</strong> ${emotion.toUpperCase()} ${emojiMap[emotion]}</p>
        `;
        showModal(modalContent);
    };

    const showModal = (htmlContent) => {
        modalText.innerHTML = htmlContent;
        modal.style.display = 'flex';
        videoPlayer.pause();
    };

    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
        videoPlayer.play();
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
            videoPlayer.play();
        }
    });

    toggleModeButton.addEventListener('click', () => {
        isEmotionMode = !isEmotionMode;
        toggleModeButton.textContent = isEmotionMode ? 'Toggle Normal Subtitles' : 'Toggle Emotion Colors';
    });

});