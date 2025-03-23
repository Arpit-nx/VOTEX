document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData();
    const audioFile = document.getElementById('audioFile').files[0];
    const language = document.getElementById('language').value;
    formData.append('audio', audioFile);
    formData.append('language', language);

    fetch('/translate', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('error').textContent = data.error;
        } else {
            document.getElementById('inputText').textContent = data.input_text;
            document.getElementById('translatedText').textContent = data.translated_text;
            const audioPlayback = document.getElementById('audioPlayback');
            audioPlayback.src = data.audio_file;
            audioPlayback.style.display = 'block';
        }
    })
    .catch(error => {
        document.getElementById('error').textContent = 'An error occurred: ' + error.message;
    });
});
