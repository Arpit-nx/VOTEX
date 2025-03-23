document.addEventListener("DOMContentLoaded", function () {
    const languageSelect = document.getElementById("language");
    const recordButton = document.getElementById("record-button");
    const stopButton = document.getElementById("stop-button");
    const fileUpload = document.getElementById("file-upload");
    const recognizedText = document.getElementById("recognized-text");
    const translatedText = document.getElementById("translated-text");
    const translatedAudio = document.getElementById("translated-audio");

    let mediaRecorder;
    let audioChunks = [];

    // Ensure all elements exist
    if (!recordButton || !stopButton || !fileUpload || !languageSelect) {
        console.error("One or more elements are missing in the DOM.");
        return;
    }

    // Function to send audio data to the server
    function sendAudioToServer(audioBlob, filename = "recorded_audio.webm") {
        const formData = new FormData();
        formData.append("audio", audioBlob, filename);
        formData.append("language", languageSelect.value);

        fetch("/translate", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.recognized_text) {
                recognizedText.textContent = data.recognized_text;
            }
            if (data.translated_text) {
                translatedText.textContent = data.translated_text;
            }
            if (data.audio_file) {
                translatedAudio.src = data.audio_file;
                translatedAudio.style.display = "block";
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while processing the audio.");
        });
    }

    // Start Recording
    recordButton.addEventListener("click", async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
            audioChunks = [];

            mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
                sendAudioToServer(audioBlob);
            };

            mediaRecorder.start();
            recordButton.disabled = true;
            stopButton.disabled = false;
        } catch (error) {
            console.error("Microphone access error:", error);
            alert("Microphone access is required to record audio.");
        }
    });

    // Stop Recording
    stopButton.addEventListener("click", () => {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            recordButton.disabled = false;
            stopButton.disabled = true;
        }
    });

    // Handle File Upload
    fileUpload.addEventListener("change", event => {
        const file = event.target.files[0];
        if (file) {
            sendAudioToServer(file, file.name);
        }
    });
});
