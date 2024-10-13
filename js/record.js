let mediaRecorder;
let audioChunks = [];
const startRecordBtn = document.getElementById('startRecord');
const stopRecordBtn = document.getElementById('stopRecord');
// const audioPlayback = document.getElementById('audioPlayback');
const transcriptionOutput = document.getElementById('transcriptionOutput'); // Output element for transcription
let stream;

// Start recording
    startRecordBtn.addEventListener('click', async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    // Capture audio data in chunks
    mediaRecorder.ondataavailable = event => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.onstop = async () => {
      try {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const arrayBuffer = await audioBlob.arrayBuffer();

        // Use audioContext to decode and encode the audio data
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

        const wavBuffer = encodeWAV(audioBuffer);
        const pcmWavBlob = new Blob([wavBuffer], { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('file', pcmWavBlob, 'recording.wav'); // Append audio as 'file'

        fetch('http://127.0.0.1:8001/transcribe', {
            method: 'POST',
            body: formData,
            headers: {
              'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.transcription) {
                console.log('Transcription:', data.transcription);
                transcriptionOutput.textContent = data.transcription; // Display the transcription in the output element
            } else if (data.error) {
                console.error('Error:', data.error);
                transcriptionOutput.textContent = 'Error transcribing audio';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            transcriptionOutput.textContent = 'Error transcribing audio';
        });

        // Clear audio chunks for the next recording
        audioChunks = [];
      } catch (error) {
        console.error('Error during recording processing:', error);
      }
    };

    mediaRecorder.start(1000); // Record in chunks of 1 second
    startRecordBtn.disabled = true;
    stopRecordBtn.disabled = false;
  } catch (error) {
    console.error('Error accessing audio stream:', error);
  }
});

// Stop recording
stopRecordBtn.addEventListener('click', () => {
  mediaRecorder.stop();
  stream.getTracks().forEach(track => track.stop()); // Stop all tracks of the media stream
  stream = null; // Release the media stream
  startRecordBtn.disabled = false;
  stopRecordBtn.disabled = true;
});

// Function to encode audio buffer to WAV format
function encodeWAV(audioBuffer) {
  const numberOfChannels = audioBuffer.numberOfChannels;
  const sampleRate = audioBuffer.sampleRate;
  const length = audioBuffer.length * numberOfChannels * 2 + 44;
  const buffer = new ArrayBuffer(length);
  const view = new DataView(buffer);

  // Write WAV header
  writeString(view, 0, 'RIFF');
  view.setUint32(4, 36 + audioBuffer.length * numberOfChannels * 2, true);
  writeString(view, 8, 'WAVE');
  writeString(view, 12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, numberOfChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * numberOfChannels * 2, true);
  view.setUint16(32, numberOfChannels * 2, true);
  view.setUint16(34, 16, true);
  writeString(view, 36, 'data');
  view.setUint32(40, audioBuffer.length * numberOfChannels * 2, true);

  // Write audio data
  let offset = 44;
  for (let i = 0; i < audioBuffer.length; i++) {
    for (let channel = 0; channel < numberOfChannels; channel++) {
      const sample = audioBuffer.getChannelData(channel)[i];
      view.setInt16(offset, sample * 0x7FFF, true);
      offset += 2;
    }
  }

  return buffer;
}

function writeString(view, offset, string) {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i));
  }
}