// Get the language select element
const languageSelect = document.getElementById('language');

// Get the record and stop button elements
const recordButton = document.getElementById('record-button');
const stopButton = document.getElementById('stop-button');

// Initialize variables
let recording = false;
let audioContext;
let stream;
let chunks = [];

// Add event listener to record button
recordButton.addEventListener('click', async () => {
  if (!recording) {
    recording = true;
    recordButton.disabled = true;
    stopButton.disabled = false;

    // Create a new audio context
    audioContext = new AudioContext();
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaStreamSource = audioContext.createMediaStreamSource(stream);
    const audioChunks = [];

    // Connect the media stream source to the audio context destination
    mediaStreamSource.connect(audioContext.destination);

    // Add event listeners to the stream
    stream.onactive = () => {
      console.log('Stream active');
    };

    stream.oninactive = () => {
      console.log('Stream inactive');
    };

    // Define a function to handle audio processing
    const handleAudioProcess = (event) => {
      audioChunks.push(event.data);
    };

    // Add the audio processing function to the media stream source
    mediaStreamSource.onaudioprocess = handleAudioProcess;
  }
});

// Add event listener to stop button
stopButton.addEventListener('click', async () => {
  if (recording) {
    recording = false;
    recordButton.disabled = false;
    stopButton.disabled = true;

    // Stop the stream tracks
    stream.getTracks().forEach((track) => {
      track.stop();
    });

    // Create a blob from the audio chunks
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append('audio', audioBlob);
    formData.append('language', languageSelect.value);

    // Send the audio data to the server for translation
    fetch('/translate', {
      method: 'POST',
      body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      // Display the translated text and audio file path
      const translatedTextElement = document.getElementById('translated-text');
      translatedTextElement.textContent = data.translated_text;

      const audioFileElement = document.getElementById('audio-file');
      audioFileElement.href = data.audio_file;
      audioFileElement.textContent = 'Listen to translated audio';
    })
    .catch((error) => {
      console.error(error);
    });
  }
});