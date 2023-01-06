def hex_to_pretty_mac(mac):
    mac = hex(int(mac)).split('x')[1].zfill(12)
    return ':'.join(''.join(x) for x in zip(*[iter(mac)]*2))

# See https://stackoverflow.com/questions/62827560/caesar-cipher-code-in-python-convert-to-unicode-shift-value-then-return-back
def caesar_encrypt(text, k):
    return ''.join(chr((ord(ch) + k) % 0x10FFFF) for ch in text)

def caesar_decrypt(ciphertext, k):
    return ''.join(chr((ord(ch) - k) % 0x10FFFF) for ch in ciphertext)