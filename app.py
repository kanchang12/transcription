from flask import Flask, render_template, request, jsonify
from google.cloud import speech_v1p1beta1 as speech
from google.auth import default
import os

app = Flask(__name__)

# Obtain the default credentials
credentials, project = default()

speech_client = speech.SpeechClient(credentials=credentials)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        # Get audio data from request
        audio_data = request.data

        # Log the audio data for debugging
        print(f"Audio data length: {len(audio_data)}")

        # Configure recognition settings with enhanced model
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            model="video",  # Use an enhanced model
            use_enhanced=True
        )
        audio = speech.RecognitionAudio(content=audio_data)

        # Make recognize request
        response = speech_client.recognize(config=config, audio=audio)

        # Log the response for debugging
        print(f"Response: {response}")

        # Extract and return transcription
        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript + "\n"

        return jsonify(transcription=transcription.strip())

    except Exception as e:
        print(f"Error: {e}")
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
