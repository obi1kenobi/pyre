import socket
import string

class WifiMouseDriver:

    ACTION_KEYS = {
        'TAB': 'TAB',
        'ENTER': 'RTN',
        'ESCAPE': 'ESC',
        'PAGE_UP': 'PGUP',
        'PAGE_DOWN': 'PGDN',
        'END': 'END',
        'HOME': 'HOME',
        'LEFT': 'LF',
        'UP': 'UP',
        'RIGHT': 'RT',
        'DOWN': 'DW',
        'BACK_SPACE': 'BAS',
        'F1': 'F1',
        'F2': 'F2',
        'F3': 'F3',
        'F4': 'F4',
        'F5': 'F5',
        'F6': 'F6',
        'F7': 'F7',
        'F8': 'F8',
        'F9': 'F9',
        'F10': 'F10',
        'F11': 'F11',
        'F12': 'F12',
        'CONTROL': 'CTRL',
        'ALT': 'ALT',
        'SHIFT': 'SHIFT',
    }

    SERVER_PORT = 1978

    def __init__(self, ip):
        self._ip = ip
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip, WifiMouseDriver.SERVER_PORT))
        self._socket.setblocking(1)

    def _send(self, data):
        print "sending: " + data
        self._socket.send(data)


    def left_click(self):
        self._send("mos  1c")
        return self

    def right_click(self):
        self._send("mos  5R r d")
        self._send("mos  5R r u")
        return self

    def move_mouse(self, deltaX, deltaY):
        # maximum movement is 99 in any direction
        currX = deltaX
        if deltaX > 0:
            while currX > 0:
                moveX = min(currX, 99)
                self._send("mos  " + str(len(str(moveX)) + len(str(0)) + 3) + "m " + str(moveX) + " " + str(0))
                currX -= moveX
        elif deltaX < 0:
            while currX < 0:
                moveX = max(currX, -99)
                self._send("mos  " + str(len(str(moveX)) + len(str(0)) + 3) + "m " + str(moveX) + " " + str(0))
                currX -= moveX

        currY = deltaY
        if deltaY > 0:
            while currY > 0:
                moveY = min(currY, 99)
                self._send("mos  " + str(len(str(0)) + len(str(moveY)) + 3) + "m " + str(0) + " " + str(moveY))
                currY -= moveY
        elif deltaY < 0:
            while currY < 0:
                moveY = max(currY, -99)
                self._send("mos  " + str(len(str(0)) + len(str(moveY)) + 3) + "m " + str(0) + " " + str(moveY))
                currY -= moveY

        return self

    def typeText(self, text):
        format = "key  "
        for char in text:
            self._send(format + str(len(char)) + char)
        return self

    def press_action_key(self, name, shift=False, ctrl=False, alt=False):
        if name not in WifiMouseDriver.ACTION_KEYS:
            raise ValueError('Unknown action key name: %s' % name)

        format = "key  "
        command = str(WifiMouseDriver.ACTION_KEYS[name])
        self._send(format + str(len(command)) + command)
        return self

    def close(self):
        self._socket.close()
