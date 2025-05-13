from flask import Flask, render_template, request, jsonify
import time
import requests
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from dotenv import load_dotenv
from constants.global_values import VOICE_ID
from constants.global_values import username,hostname,password,database,port

load_dotenv()


app = Flask(__name__)
app.config['AUDIO_FOLDER'] = 'static/audio'
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    from src.agents.query_agent import QueryAgent
    from src.agents.response_agent import ResponseAgent

    # Simulate thinking delay
    # time.sleep(1.5)
    # Passing this message to agent
    query_agent = QueryAgent()
    response_agent = ResponseAgent(database=database,hostname=hostname,password=password,port=port,username=username)
    query = query_agent.get_query(query=user_message)
    print(f"sql query : {query}")
    response = response_agent.get_response(query=query)
    print(f"response : {response}")
    # Call ElevenLabs TTS API
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": response,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.7,
            "speed": 0.7
        }
    }

    r = requests.post(url, headers=headers, json=payload)
    if r.status_code != 200:
        return jsonify({'response': response, 'audio_url': None})

    # Save audio to static/audio/response.mp3
    audio_path = os.path.join(app.config['AUDIO_FOLDER'], 'response.mp3')
    with open(audio_path, 'wb') as f:
        f.write(r.content)

    # Return response text and audio file URL
    return jsonify({
        'response': response,
        'audio_url': '/static/audio/response.mp3'
    })

if __name__ == '__main__':

    print("Starting Flask application...")
    try:
        app.run(debug=True)
        print("Flask application is running")
    except Exception as e:
        print(f"Failed to start Flask: {str(e)}")