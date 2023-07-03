import os
import json
import re

import os
import json
import re

# Define the directory containing the TXT files
input_dir = '/Users/thomasrooth/google-cloud-sdk/lib/surface/components/repositories/RoothlessGPT/Thompa/Roothless_Tech/Data/Export/'
output_dir = '/Users/thomasrooth/google-cloud-sdk/lib/surface/components/repositories/RoothlessGPT/Thompa/Roothless_Tech/JSON/'

# Create the output directory if it does not exist
os.makedirs(output_dir, exist_ok=True)

# Define the filename pattern
filename_pattern = re.compile(r'\d{12,20}-history\.txt$')

# List to store all messages
all_messages = []

# Loop through the files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is a TXT file
    if filename_pattern.search(filename):
        # Construct the full path to the TXT file
        input_file = os.path.join(input_dir, filename)
        # Construct the full path to the output file
        output_file = os.path.join(output_dir, filename.replace('-history.txt', '-history.json'))

        # Open the TXT file and read the lines
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()

        # List to store the messages
        messages = []

        # Loop through the lines
        for line in lines:
            # Remove leading and trailing whitespace
            line = line.strip()

            # Check if the line contains a colon
            if ':' in line:
                # Split the line into the name, timestamp, and the message
                name, timestamp, message = line.split('(', 1)[0], line.split('(', 1)[1].split(')', 1)[0], line.split(')', 1)[1][1:]
                # Add the message to the messages list
                messages.append({'name': name.strip(), 'timestamp': timestamp.strip(), 'message': message.strip()})

        # Add the messages to the all_messages list
        all_messages.extend(messages)

        # Open the output file and write the messages to it in JSON format
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(messages, outfile, ensure_ascii=False, indent=4)

# Construct the full path to the all history file
all_history_file = os.path.join(output_dir, 'all-history.json')

# Open the all history file and write all messages to it in JSON format
with open(all_history_file, 'w', encoding='utf-8') as outfile:
    json.dump(all_messages, outfile, ensure_ascii=False, indent=4)
