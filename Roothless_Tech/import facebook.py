import os
from bs4 import BeautifulSoup

# Define the directory containing the subdirectories
inbox_dir = 'Roothless_Tech/Data/Import/facebook-thomasrooth/'
output_dir = 'Roothless_Tech/Data/Export/'

# Loop through the subdirectories in the inbox directory
for subdir in os.listdir(inbox_dir):
    # Construct the full path to the HTML file
    import_file = os.path.join(inbox_dir, subdir, 'your_event_responses.html')
    # Construct the full path to the output file
    output_file = os.path.join(output_dir, f'{subdir}-your_event_responses.txt')

    # Check if the HTML file exists
    if os.path.isfile(import_file):
        with open(import_file, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Find all message divs
        message_divs = soup.find_all('div', {'class': '_3-95 _a6-g'})

        # Dictionary to keep track of anonymous names
        anonymous_names = {}
        anonymous_counter = 1

        # List to store the messages
        messages = []

        # Loop through the message divs
        for div in message_divs:
            # Find the name div
            name_div = div.find('div', {'class': '_2ph_ _a6-h _a6-i'})
            # If the name div exists, get its text
            if name_div is not None:
                name = name_div.get_text()

                # If the message is from you, keep your name
                if 'Thomas G Rooth' in name:
                    sender = 'Thomas G Rooth'
                    recipient = name.replace('Thomas G Rooth commented on ', '').split("'s")[0]
                    # If the recipient is not in the dictionary, add it
                    if recipient not in anonymous_names:
                        anonymous_names[recipient] = f'Receiver #{anonymous_counter}'
                        anonymous_counter += 1
                    recipient = anonymous_names[recipient]
                else:
                    continue

                # Find the message div
                message_div = div.find('div', {'class': '_2pin'})
                # If the message div exists, get its text
                if message_div is not None:
                    message = message_div.get_text() 

                    # Find the date div
                    date_div = div.find('div', {'class': '_3-94 _a6-o'}).find('a')
                    # If the date div exists, get its text
                    if date_div is not None:
                        date = date_div.get_text()

                    # Add the sender, the recipient, the date, and the message to the messages list
                    messages.append(f'{sender} to {recipient} ({date}): {message}\n\n')

        # Reverse the order of the messages
        messages.reverse()
        print(len(messages)) 
        # Open the output file and write the messages to it
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(messages)
