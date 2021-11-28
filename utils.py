from pynput.keyboard import Key
def get_index_fingers(finger):
    switcher = {
        "CAI": (4, 5),
        "TRO": (8,6),
        "GIUA": (12, 10),
        "NHAN": (16, 14),
        "UT": (20, 14),
        "CHUOTTRAI": (8,11),
        "CHUOTPHAI": (16,11),
        "CUON": (8,11)
    }

    return switcher.get(finger)

def get_name_key(name):
    switcher = {
        "Tab": Key.tab,
        "Caps": Key.caps_lock,
        "Space": Key.space,
        "Enter": Key.enter,
        "Del": Key.backspace
    }

    return switcher.get(name)

class KeyButton:
    def __init__(self, posStart, posEnd, char):
        self.posStart = posStart
        self.posEnd = posEnd
        self.char = char
