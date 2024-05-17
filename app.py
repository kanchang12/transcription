from flask import Flask, render_template, request, jsonify
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account


app = Flask(__name__)



speech_client = speech.SpeechClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        # Get audio data from request
        audio_data = request.files['audioFile'].read()

        # Make a speech:recognize request using Google Cloud Speech-to-Text API
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US"  # Adjust language code as needed
        )
        audio = speech.RecognitionAudio(content=audio_data)

        #print("audio_data", audio_data)
        #print("audio", audio)

        print("Now call")

        # Make recognize request
        response = speech_client.recognize(config=config, audio=audio)

        print("called")

        print("respo", response)

        

        # Extract and return transcription
        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript + "\n"
        print("transcription", transcription)

        return jsonify(transcription=transcription.strip())
        

    except Exception as e:
        return jsonify(error=str(e)), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
