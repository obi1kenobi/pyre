import socket
import string
from driver import driver

SEP = chr(0x1e)
END = chr(0x04)

class MMLiteDriver(driver):

    TAB = "TAB"
    ENTER = "ENTER"
    BACK_SPACE = "BACKSPACE"

    ACTION_KEYS = {
        'TAB': TAB,
        'ENTER': ENTER,
        'ESCAPE': "ESCAPE",
        'PAGE_UP': "PGUP",
        'PAGE_DOWN': "PGDN",
        'END': "END",
        'HOME': "HOME",
        'LEFT': "LEFT",
        'UP': "UP",
        'RIGHT': "RIGHT",
        'DOWN': "DOWN",
        'BACK_SPACE': BACK_SPACE,
        'F1': "F1",
        'F2': "F2",
        'F3': "F3",
        'F4': "F4",
        'F5': "F5",
        'F6': "F6",
        'F7': "F7",
        'F8': "F8",
        'F9': "F9",
        'F10': "F10",
        'F11': "F11",
        'F12': "F12"
    }

    TRANSLATION_TABLE = {
        '\n': ENTER,
        '\b': BACK_SPACE,
        '\t': TAB
    }

    SERVER_PORT = 9090

    def __init__(self, ip):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip, MMLiteDriver.SERVER_PORT))
        self._connect()

    def close(self):
        self._socket.close()

    def _connect(self):
        # connect_hex says something along the lines of "CONNECT[SEP][SEP]ANDROID[SEP]ANDROID[SEP]2.0.6[SEP]0[END]"
        connect_hex = [0x43, 0x4f, 0x4e, 0x4e, 0x45, 0x43, 0x54, 0x1e, 0x1e, 0x41, 0x6e, 0x64, 0x72, 0x6f, 0x69, 0x64, 0x1e, 0x41, 0x6e, 0x64, 0x72, 0x6f, 0x69, 0x64, 0x1e, 0x32, 0x2e, 0x30, 0x2e, 0x36, 0x1e, 0x30, 0x04]
        s = ''
        for num in connect_hex:
            s += chr(num)
        self._send(s)

    def _send(self, data):
        print "sending: " + data
        self._socket.sendall(data)

    def left_click(self):
        self._send(SEP.join(["CLICK", "L", "D", END]))
        self._send(SEP.join(["CLICK", "L", "U", END]))
        return self

    def right_click(self):
        self._send(SEP.join(["CLICK", "R", "D", END]))
        self._send(SEP.join(["CLICK", "R", "U", END]))
        return self

    def move_mouse(self, deltaX, deltaY):
        # maximum movement is 50 in any direction
        currX = deltaX
        if deltaX > 0:
            while currX > 0:
                moveX = min(currX, 50)
                self._send(SEP.join(["MOVE", str(float(moveX)), str(0), "0", END]))
                currX -= moveX
        elif deltaX < 0:
            while currX < 0:
                moveX = max(currX, -50)
                self._send(SEP.join(["MOVE", str(float(moveX)), str(0), "0", END]))
                currX -= moveX

        currY = deltaY
        if deltaY > 0:
            while currY > 0:
                moveY = min(currY, 50)
                self._send(SEP.join(["MOVE", str(0), str(float(moveY)), "0", END]))
                currY -= moveY
        elif deltaY < 0:
            while currY < 0:
                moveY = max(currY, -50)
                self._send(SEP.join(["MOVE", str(0), str(float(moveY)), "0", END]))
                currY -= moveY

        return self

    def typeText(self, text):
        for c in text:
            if c in MMLiteDriver.TRANSLATION_TABLE:
                c = MMLiteDriver.TRANSLATION_TABLE[c]
            self._send(SEP.join(["KEY", "-1", c, END]))
        return self

    def press_action_key(self, name, shift=False, ctrl=False, alt=False):
        code = None
        if name in MMLiteDriver.ACTION_KEYS:
            code = MMLiteDriver.ACTION_KEYS[name]
        else:
            code = name

        keys = []
        if shift:
            keys.append('SHIFT')
        if ctrl:
            keys.append('CTRL')
        if alt:
            keys.append('ALT')
        keys_str = '+'.join(keys)

        self._send(SEP.join(["KEY", "-1", code, keys_str, END]))
        
        return self
