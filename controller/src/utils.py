from pyfiglet import Figlet
from datetime import datetime

figlet = Figlet()


def jumbo_text(text):
    return figlet.renderText(text)


def hex_to_pretty_mac(mac):
    mac = hex(int(mac)).split('x')[1].zfill(12)
    return ':'.join(''.join(x) for x in zip(*[iter(mac)]*2))


# See https://gist.github.com/rosenhouse/a0307caf0a1d2b26116b
def time_ago(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc

    Modified from: http://stackoverflow.com/a/1551394/141084
    """
    now = datetime.utcnow()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = 0
    else:
        raise ValueError('invalid date %s of type %s' % (time, type(time)))
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"

    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff//7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff//30) + " months ago"
    return str(day_diff//365) + " years ago"


# See https://stackoverflow.com/questions/40419276/python-how-to-print-text-to-console-as-hyperlink
def link(uri, label=None):
    if label is None:
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)


# See https://stackoverflow.com/questions/62827560/caesar-cipher-code-in-python-convert-to-unicode-shift-value-then-return-back
def caesar_encrypt(text, k):
    return ''.join(chr((ord(ch) + k) % 0x10FFFF) for ch in text)


def caesar_decrypt(ciphertext, k):
    return ''.join(chr((ord(ch) - k) % 0x10FFFF) for ch in ciphertext)
