import requests

# Define the URL
url = 'http://127.0.0.1:5000/chat'

# Define the data to send
data = {
    'message': 'majs'
}

# Send the POST request and get the response
response = requests.post(url, json=data)

# Print the response
print(response.json())
