from alive import heartbeat
from commander import check_pending_commands

def main():
    heartbeat()
    check_pending_commands()


if __name__ == "__main__":
    main()
