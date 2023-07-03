from flask import Flask, request, jsonify, render_template, session, 
import openai
import os
import json
import secrets
print(secrets.token_hex(16))

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Load chat logs and bio data at the start of the application
with open('Roothless_Tech/JSON/chatlog.json') as f:
    chatlog_data = json.load(f)

with open('Roothless_Tech/JSON/bio.json') as f:
    bio_data = json.load(f)

@app.route('/init_chat', methods=['GET'])
def init_chat():
    session['messages'] = []  # Initialize messages in the user's session

    # Prepare the messages list with system and user prompts
    session['messages'].extend([
        {"role": "system", "content": "You are Chat GPT. A helpful AI Assistant that have the ability to act like you have incredible acting and writing skills"},
        {"role": "user", "content": "I want you to act like Thomas G Rooth based on 'Roothless_Tech/JSON/bio.json' and 'Roothless_Tech/JSON/chatlog.json'. I want you to respond and answer like Thomas G Rooth using the tone, manner and vocabulary Thomas G Rooth would use. Do not write any explanations. Only answer like Thomas G Rooth. You must know all of the knowledge of Thomas G Rooth. My first sentence is: Hi Thomas G Rooth"}
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

    return jsonify({"response": response.choices[0].message['content']})


@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json['message']

    session['messages'].append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=session['messages']
    )

    response_text = response.choices[0].message['content']
    session['messages'].append({"role": "assistant", "content": response_text})

    return jsonify({"response": response_text})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
