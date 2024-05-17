from flask import Flask, render_template, request, jsonify
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

app = Flask(__name__)

"""

# Define the service account key dictionary
service_key = {
  "type": "service_account",
  "project_id": "<project_id>",
  "private_key_id": "<private_key_id>",
  "private_key": "<private_key>",
  "client_email": "<client_email>",
  "client_id": "<client_id>",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "<client_x509_cert_url>"
}
"""

# Create credentials using the service account key
credentials = "1650f89760684e28d699210f32eead6c46e07bc4"

# Set the credentials globally for all Google Cloud services
speech_client = speech.SpeechClient(credentials=credentials)

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

        """

        # Extract and return transcription
        transcription = ""
        for result in response.results:
            transcription += result.alternatives[0].transcript + "\n"
        print("transcription", transcription)

        return jsonify(transcription=transcription.strip())
        """

    except Exception as e:
        return jsonify(error=str(e)), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
