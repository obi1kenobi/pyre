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

    def _listen_for_replies(self):
        try:
            data, addr = self._input_socket.recvfrom(1024)
            print "%s replied: %s" % (addr, data)
            return True
        except:
            return False

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
        self._send("mos  " + str(len(str(deltaX)) + len(str(deltaY)) + 3) + "m " + str(deltaX) + " " + str(deltaY))
        return self

    def type(self, text):
        format = "utf8  "
        hexstring = "0a"
        result = hexstring.decode("hex")
        self._send(format + text + result);
        return self

    def press_action_key(self, name, shift=False, ctrl=False, alt=False):
        if name not in WifiMouseDriver.ACTION_KEYS:
            raise ValueError('Unknown action key name: %s' % name)

        format = "key  "
        command = str(WifiMouseDriver.ACTION_KEYS[name])
        self._send(format + str(len(command)) + " " + command)
        return self

    def ping(self):
        format = "from:airhid"
        self._send(format)
        return self._listen_for_replies()

    def close(self):
        self._socket.close()
