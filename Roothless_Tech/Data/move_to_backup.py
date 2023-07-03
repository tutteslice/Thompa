import shutil
import os

# define the source and destination directories
source_dir = 'Roothless_Tech/Data/Import/facebook-thomasrooth/messages/inbox/'
dest_dir = 'Roothless_Tech/Data/Export/backup/'

# walk through the source directory
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # only process 'message_1.html' files
        if file == 'message_1.html':
            # construct the full file path
            source_file = os.path.join(root, file)
            # construct the destination file path
            dest_file = os.path.join(dest_dir, os.path.relpath(source_file, source_dir))
            # create the destination directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            # move the file to the destination directory
            shutil.move(source_file, dest_file)