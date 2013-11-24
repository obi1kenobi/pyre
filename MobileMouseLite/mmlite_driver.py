import socket
import string

SEP = chr(0x1e)
END = chr(0x04)

class MMLiteDriver:

    def __init__(self, ip, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip, port))

    def connect(self):
        # connect_hex says something along the lines of "CONNECTANDROIDANDROID2.0.6"
        connect_hex = [0x43, 0x4f, 0x4e, 0x4e, 0x45, 0x43, 0x54, 0x1e, 0x1e, 0x41, 0x6e, 0x64, 0x72, 0x6f, 0x69, 0x64, 0x1e, 0x41, 0x6e, 0x64, 0x72, 0x6f, 0x69, 0x64, 0x1e, 0x32, 0x2e, 0x30, 0x2e, 0x36, 0x1e, 0x30, 0x04]
        s = ''
        for num in connect_hex:
            s += chr(num)
        self._send(s)

    def close(self):
        self._socket.close()

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

    def type(self, text):
        for c in text:
            if c == '\n':
                c = 'ENTER'
            self._send(SEP.join(["KEY", "-1", c, END]))
        return self

    def press_action_key(self, key, shift=False, ctrl=False, alt=False):
        keys = []
        if shift:
            keys.append('SHIFT')
        if ctrl:
            keys.append('CTRL')
        if alt:
            keys.append('ALT')
        keys_str = '+'.join(keys)

        self._send(SEP.join(["KEY", "-1", key, keys_str, END]))
        
        return self