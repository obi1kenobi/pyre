import socket
import string

class RemoteMouseDriver:

    SHIFT = "shift"
    CTRL = "ctrl"
    ALT = "alt"

    TAB = "tab"
    ENTER = "RTN"
    BACK_SPACE = "BAS"

    ACTION_KEYS = {
        'TAB': TAB,
        'ENTER': ENTER,
        'ESCAPE': "esc",
        'PAGE_UP': "pageup",
        'PAGE_DOWN': "pagedown",
        'END': "end",
        'HOME': "home",
        'LEFT': "LF",
        'UP': "UP",
        'RIGHT': "RT",
        'DOWN': "DW",
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

    SERVER_PORT = 1978

    def __init__(self, ip):
        self._output_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._output_socket.connect((ip, RemoteMouseDriver.SERVER_PORT))

    def _send(self, data):
        print "sending: " + data
        self._output_socket.sendall(data)

    def _get_char_code(self, c):
        if c in RemoteMouseDriver.TRANSLATION_TABLE:
            return RemoteMouseDriver.TRANSLATION_TABLE[c]
        else:
            code = "[ras]" + str(ord(c) ^ 53)
            code = str(len(code)) + code
            return code

    def left_click(self):
        self._send("mos  5R l d")
        self._send("mos  5R l u")
        return self

    def right_click(self):
        self._send("mos  5R r d")
        self._send("mos  5R r u")
        return self

    def scroll_up(self):
        self._send("mos  3w 1")
        return self

    def scroll_down(self):
        self._send("mos  3w 0")
        return self

    def move_mouse(self, deltaX, deltaY):
        self._send("mos  m " + str(deltaX) + " " + str(deltaY))
        return self

    def type(self, text):
        format = "key  "
        code = None
        for c in text:
            code = self._get_char_code(c)
            self._send(format + code)
        return self

    def press_action_key(self, name, shift=False, ctrl=False, alt=False):
        code = None
        if name in RemoteMouseDriver.ACTION_KEYS:
            code = RemoteMouseDriver.ACTION_KEYS[name]
        elif len(name) == 1:
            code = name
        else:
            raise ValueError('Cannot send key stroke: %s' % name)
        if (shift and ctrl) or (shift and alt) or (ctrl and alt):
            raise ValueError('Cannot send more than one modifier at a time: shift=%s, ctrl=%s, alt=%s' % \
                (str(shift), str(ctrl), str(alt)))

        command = ''
        if shift:
            command = RemoteMouseDriver.SHIFT + '[+]'
        if ctrl:
            command = RemoteMouseDriver.CTRL + '[+]'
        if alt:
            command = RemoteMouseDriver.ALT + '[+]'

        command += RemoteMouseDriver.ACTION_KEYS[name]

        self._send(command)
        return self
