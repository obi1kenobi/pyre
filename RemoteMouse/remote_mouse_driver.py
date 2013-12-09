import socket
import string
import hashlib

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
    MOUSE_COMMAND_PREFIX = "mos"
    KEY_COMMAND_PREFIX = "key"
    PASSWORD_INPUT_PREFIX = "cin"

    def __init__(self, ip):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip, RemoteMouseDriver.SERVER_PORT))
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self._execute_handshake()

    def _pad_length(self, length):
        res = str(length)
        while len(res) < 3:
            res = ' ' + res
        return res

    def _execute_handshake(self):
        info = self._socket.recv(1024)
        print "received:", info

        tokens = info[6:].split(' ')
        print "INFO: Version", tokens[-1]
        if 'win' in tokens:
            print "INFO: Windows server"
        if 'pwd' in tokens:
            hash_challenge = tokens[-2].strip()
            print "INFO: Password required, challenge MD5 hash", hash_challenge

            # take hash challenge in hex, reverse it and hash it with md5 (no salt)
            # this is the response to the challenge
            h = hashlib.new('md5')
            h.update(hash_challenge[::-1])
            response = h.hexdigest()

            print "INFO: Sending computed response", response
            self._send(RemoteMouseDriver.PASSWORD_INPUT_PREFIX, response)
        elif 'nopwd' in info:
            print "INFO: No password required"

    def _send(self, prefix, command):
        data = prefix + self._pad_length(len(command)) + command
        print "sending: " + data
        self._socket.sendall(data)

    def _get_char_code(self, c):
        if c in RemoteMouseDriver.TRANSLATION_TABLE:
            return RemoteMouseDriver.TRANSLATION_TABLE[c]
        else:
            code = "[ras]" + str(ord(c) ^ 53)
            code = str(len(code)) + code
            return code

    def left_click(self):
        self._send(RemoteMouseDriver.MOUSE_COMMAND_PREFIX, "R l d")
        self._send(RemoteMouseDriver.MOUSE_COMMAND_PREFIX, "R l u")
        return self

    def right_click(self):
        self._send(RemoteMouseDriver.MOUSE_COMMAND_PREFIX, "R r d")
        self._send(RemoteMouseDriver.MOUSE_COMMAND_PREFIX, "R r u")
        return self

    def scroll_up(self):
        self._send(RemoteMouseDriver.MOUSE_COMMAND_PREFIX, "w 1")
        return self

    def scroll_down(self):
        self._send(RemoteMouseDriver.MOUSE_COMMAND_PREFIX, "w 0")
        return self

    def move_mouse(self, deltaX, deltaY):
        self._send(RemoteMouseDriver.MOUSE_COMMAND_PREFIX, "m " + str(deltaX) + " " + str(deltaY))
        return self

    def typeText(self, text):
        code = None
        for c in text:
            code = self._get_char_code(c)
            self._send(RemoteMouseDriver.KEY_COMMAND_PREFIX, code)
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

        self._send(RemoteMouseDriver.KEY_COMMAND_PREFIX, command)
        return self
