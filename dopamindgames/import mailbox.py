import mailbox
import email

mbox_file = 'Roothless_Tech/Data/Import/mail0'
email_addresses = ('thomasrooth.90@gmail.com','Thomas Rooth <thomasrooth.90@gmail.com>','thomas.rooth@ist.com','<thomas.rooth@ist.com>','Thomas Rooth thomas.rooth@ist.com')
output_file = 'Roothless_Tech/Data/Export/mailhistorik.txt'
def get_text_from_email(msg):
    parts = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                charset = part.get_content_charset() or 'utf-8'  # Use 'utf-8' if the charset is not specified
                parts.append(part.get_payload(decode=True).decode(charset, errors='replace'))
                break  # Only get the first part
    elif msg.get_content_type() == 'text/plain':
        charset = msg.get_content_charset() or 'utf-8'
        parts.append(msg.get_payload(decode=True).decode(charset, errors='replace'))
    return ''.join(parts)


# Open the output file in write mode
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Open the mbox file using the mailbox module
    mbox = mailbox.mbox(mbox_file)
    
    # Loop through all the messages in the mbox file
    for index, message in enumerate(mbox):
        # Check if the message was sent by you
        if message['From'] in email_addresses:
            # Get the message text
            message_text = get_text_from_email(message)
            # Write the message text to the output file
            outfile.write(f'Message {index + 1}:\n{message_text}\n') 
