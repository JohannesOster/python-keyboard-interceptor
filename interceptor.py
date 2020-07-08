import keyboard
from keymap import keymap
import time

def sendChar(char):
    """
    open the /dev/hidg0 device in r+ (read and write) of binary (b) mode.
    encoding() converts provided character (in oure case this should be a sequence hex numbers)
    into bytes.
    """
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(char.encode())


def on_press(keyboard_event):
    character = keyboard_event.name
    """
    HID consists of up to 8 bytes. Visit the following link to see a detailed explanaition about
    the structure of an HID report. https://wiki.osdev.org/USB_Human_Interface_Devices

    Numbers in HID have the format \0\0{chr(usageID of digit)}\0\0\0\0\0
    The actual usage ID for a given number can be looked up in the following HDI usage Table on
    chapter "10 Keyboard/Keypad Page(0x07)" page 53
    https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf

    char(2) is the representation of the shift key. It should be at the first position of the
    HID report since it represents a "Modifier keys status". chr(2)\0{chr(usageID of char)}\0\0\0\0\0
    Therfore the character uppercase A looks like this chr(2)\0\x04\0\0\0\0\0 vs a small a \0\0\x04\0\0\0\0\0

    After sending the press key instruction. The key has to be released as well, 
    otherwise it would send the pressed key forever.
    To release a key send a HID report consiting only of null chars.

    Note: As long as the only characters this script should support are 0-9 and a-z
          char(0)*2 at as prefix can stay. If however the "Modifier keys status" has
          to be used (for example for uppercase letters) it has to be removed ant included
          in the lookup table.
          The suffix chr(0)*5 can stay.
    """
    sendChar(chr(0)*2+keymap[character]+chr(0)*5)  # press key
    sendChar(chr(0) * 8)  # releive key

def event_loop():
    """
    This function runs forever on purpose.
    It makes shure that each keyboard input is resent to /dev/hidg0
    """
    while True:
        time.sleep(1)

if __name__ == "__main__":
    print("Start keyboard emulator.")
    print("To end press Ctr+C")
    keyboard.on_press(on_press)
    event_loop()
