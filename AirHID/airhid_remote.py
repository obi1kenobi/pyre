import socket

class AirHID_Remote:
    def __init__(self, ip, port):
        self._ip = ip
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._port = port

    def _send(self, data):
        print "sending: " + data
        self._socket.sendto(data, (self._ip, self._port))

    def left_click(self):
        self._send("clk.1_DOWN")
        self._send("clk.1_UP")
        return self

    def right_click(self):
        self._send("clk.2_DOWN")
        self._send("clk.2_UP")
        return self

    def scroll_up(self):
        self._send("clk.3_UP")
        return self

    def scroll_down(self):
        self._send("clk.3_DOWN")
        return self

    def move_mouse(self, deltaX, deltaY):
        self._send("pos." + str(deltaX) + "," + str(deltaY))
        return self

    def open_url(self, url):
        self._send("url."+url)
        return self
