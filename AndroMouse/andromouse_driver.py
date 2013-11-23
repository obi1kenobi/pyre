import socket
import string

class AndroMouseDriver:

    def __init__(self, ip, port):
        self._ip = ip
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._port = port

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

    def type(self, text):
        for c in text:
            # special cases
            if c == ":":
                # hold down shift key and press semicolon
                self._send("ShiftKDwn")
                self._send(";")
                self._send("ShiftKU")
            else:
                self._send(c)
        return self

    def press_action_key(self, key, shift=False, ctrl=False, alt=False):
        if shift:
            self._send("ShiftKDwn")
        if ctrl:
            self._send("CtrlKDwn")
        if alt:
            self._send("AltKDwn")

        self._send(key)

        if shift:
            self._send("ShiftKU")
        if ctrl:
            self._send("CtrlKU")
        if alt:
            self._send("AltKU")

        return self