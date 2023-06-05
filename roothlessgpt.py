from flask import Flask, request, jsonify
import openai
import requests

openai.api_key = ''

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json['message']

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a troubled soul."},
            {"role": "user", "content": "You are a clone of Thomas Rooth, created in his image. You like to joke around and never waste an opportunity for a good joke."},
            {"role": "user", "content": "You will answer in Swedish."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return jsonify({"response": response.choices[0].message['content']})

if __name__ == '__main__':

    app.run(host='0.0.0.0')
