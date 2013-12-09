import socket
import string
from driver import driver

class AndroMouseDriver(driver):

    TAB = "TabKey"
    ENTER = "EnterKey"
    BACK_SPACE = "\b"

    ACTION_KEYS = {
        'TAB': TAB,
        'ENTER': ENTER,
        'ESCAPE': "EscKey",
        'PAGE_UP': "PgupKey",
        'PAGE_DOWN': "PgdownKey",
        'END': "EndKey",
        'HOME': "HomeKey",
        'LEFT': "LeftKey",
        'UP': "UpKey",
        'RIGHT': "RightKey",
        'DOWN': "DownKey",
        'BACK_SPACE': BACK_SPACE,
        'F1': "F1Key",
        'F2': "F2Key",
        'F3': "F3Key",
        'F4': "F4Key",
        'F5': "F5Key",
        'F6': "F6Key",
        'F7': "F7Key",
        'F8': "F8Key",
        'F9': "F9Key",
        'F10': "F10Key",
        'F11': "F11Key",
        'F12': "F12Key"
    }

    TRANSLATION_TABLE = {
        '\n': ENTER,
        '\b': BACK_SPACE,
        '\t': TAB
    }

    def __init__(self, ip, port):
        self._ip = ip
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._port = port

    def close(self):
        self._socket.close()

    def _send(self, data):
        print "sending: " + data
        self._socket.sendto(data, (self._ip, self._port))

    def left_click(self):
        self._send("click")
        return self

    def right_click(self):
        self._send("rtclk")
        return self

    def move_mouse(self, deltaX, deltaY):
        self._send(str(deltaX) + "x" + str(deltaY) + "y" + "MVEX")
        return self

    def typeText(self, text):
        for c in text:
            # special cases
            if c == ":":
                # hold down shift key and press semicolon
                self._send("ShiftKDwn")
                self._send(";")
                self._send("ShiftKU")
            else:
                if c in AndroMouseDriver.TRANSLATION_TABLE:
                    c = AndroMouseDriver.TRANSLATION_TABLE[c]
                self._send(c)
        return self

    def press_action_key(self, name, shift=False, ctrl=False, alt=False):
        code = None
        if name in AndroMouseDriver.ACTION_KEYS:
            code = AndroMouseDriver.ACTION_KEYS[name]
        else:
            code = name

        if shift:
            self._send("ShiftKDwn")
        if ctrl:
            self._send("CtrlKDwn")
        if alt:
            self._send("AltKDwn")

        self._send(code)

        if shift:
            self._send("ShiftKU")
        if ctrl:
            self._send("CtrlKU")
        if alt:
            self._send("AltKU")

        return self
