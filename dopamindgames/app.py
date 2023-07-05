from flask import Flask, request, jsonify, render_template, session
from flask_session import Session  # Correct import
import openai
import os
import json
import secrets
print(secrets.token_hex(16))

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem-based sessions
Session(app)
app.secret_key = os.getenv('SECRET_KEY')

# Load chat logs and bio data at the start of the application
with open('/Users/thomasrooth/google-cloud-sdk/lib/surface/components/repositories/RoothlessGPT/Thompa/Roothless_Tech/JSON/chatlog.json') as f:
    chatlog_data = json.load(f)

with open('/Users/thomasrooth/google-cloud-sdk/lib/surface/components/repositories/RoothlessGPT/Thompa/Roothless_Tech/JSON/bio.json') as f:
    bio_data = json.load(f)

@app.route('/init_chat', methods=['GET'])
def init_chat():
    session['messages'] = []  # Initialize messages in the user's session

    # Prepare the messages list with system and user prompts
    session['messages'].extend([
        {"role": "system", "content": "Du är Chat GPT. En hjälpsam AI-assistent som har förmågan att agera som om du har otroliga skådespelar- och skrivfärdigheter."},
        {"role": "user", "content": "Jag vill att du agerar som Thomas G Rooth baserat på 'Roothless_Tech/JSON/bio.json' och 'Roothless_Tech/JSON/chatlog.json'. Jag vill att du svarar och agerar som Thomas G Rooth skulle göra, med samma ton, manér och ordförråd som Thomas G Rooth skulle använda. Skriv inte några förklaringar. Svara endast som Thomas G Rooth. Du måste känna till all kunskap om Thomas G Rooth. Min första mening är: Hej Thomas G Rooth."}
    ])

    # Iterate over chat logs and add them as user and assistant messages
    for chatlog in chatlog_data:
        sender = chatlog['sender']
        message = chatlog['message']

        if sender == "Thomas G Rooth":
            session['messages'].append({"role": "user", "content": message})
        else:
            session['messages'].append({"role": "assistant", "content": message})

    # Add texts as user prompts
    for bio in bio_data:
        name = bio["name"]
        message = bio["message"]
        if name == "Thomas G Rooth":
            session['messages'].append({"role": "user", "content": bio})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=session['messages']
    )

    return jsonify({"response": response.choices[0].message['content']}) # type: ignore


@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json['message']

    session['messages'].append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=session['messages']
    )

    response_text = response.choices[0].message['content'] # type: ignore
    session['messages'].append({"role": "assistant", "content": response_text})

    return jsonify({"response": response_text})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
