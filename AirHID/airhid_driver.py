import socket
import string
from driver import driver

class AirHidDriver(driver):

    SHIFT = "_SHIFT"
    ALT = "_ALT"
    CTRL = "_CTRL"
    WIN = "_WIN"

    VK_CAPS_LOCK                = 0x14
    VK_ESCAPE                   = 0x1B
    VK_PAGE_UP                  = 0x21
    VK_PAGE_DOWN                = 0x22
    VK_END                      = 0x23
    VK_HOME                     = 0x24
    VK_LEFT                     = 0x25
    VK_UP                       = 0x26
    VK_RIGHT                    = 0x27
    VK_DOWN                     = 0x28
    VK_BACK_SPACE               = ord('\b')
    VK_F1                       = 0x70
    VK_F2                       = 0x71
    VK_F3                       = 0x72
    VK_F4                       = 0x73
    VK_F5                       = 0x74
    VK_F6                       = 0x75
    VK_F7                       = 0x76
    VK_F8                       = 0x77
    VK_F9                       = 0x78
    VK_F10                      = 0x79
    VK_F11                      = 0x7A
    VK_F12                      = 0x7B

    VK_ENTER                    = ord('\n')
    VK_TAB                      = ord('\t')
    VK_SPACE                    = 0x20
    VK_COMMA                    = 0x2C
    VK_MINUS                    = 0x2D
    VK_PERIOD                   = 0x2E
    VK_SLASH                    = 0x2F
    VK_SEMICOLON                = 0x3B
    VK_EQUALS                   = 0x3D
    VK_OPEN_BRACKET             = 0x5B
    VK_BACK_SLASH               = 0x5C
    VK_CLOSE_BRACKET            = 0x5D
    VK_MULTIPLY                 = 0x6A
    VK_ADD                      = 0x6B
    VK_QUOTE                    = 0xDE
    VK_AMPERSAND                = 0x96
    VK_LESS                     = 0x99
    VK_GREATER                  = 0xA0
    VK_AT                       = 0x0200
    VK_COLON                    = 0x0201
    VK_CIRCUMFLEX               = 0x0202
    VK_DOLLAR                   = 0x0203
    VK_EXCLAMATION_MARK         = 0x0205
    VK_LEFT_PARENTHESIS         = 0x0207
    VK_NUMBER_SIGN              = 0x0208
    VK_RIGHT_PARENTHESIS        = 0x020A
    VK_UNDERSCORE               = 0x020B
    VK_QUOTE                    = 0xDE

    # translation table, because AirHID's codes sometimes differ from Java's
    TRANSLATION_TABLE = {
      10: 13,
      154: 42,
      155: 45,
      127: 46,
      156: 47,
      61440: 124,
      61441: 125,
      61442: 126,
      61443: 127,
      513: 186,
      59: 187,
      44: 188,
      45: 189,
      46: 190,
      47: 191,
      512: 192,
      91: 219,
      92: 220,
      93: 221
    }

    ACTION_KEYS = {
        'TAB': VK_TAB,
        'ENTER': VK_ENTER,
        'CAPS_LOCK': VK_CAPS_LOCK,
        'ESCAPE': VK_ESCAPE,
        'PAGE_UP': VK_PAGE_UP,
        'PAGE_DOWN': VK_PAGE_DOWN,
        'END': VK_END,
        'HOME': VK_HOME,
        'LEFT': VK_LEFT,
        'UP': VK_UP,
        'RIGHT': VK_RIGHT,
        'DOWN': VK_DOWN,
        'BACK_SPACE': VK_BACK_SPACE,
        'F1': VK_F1,
        'F2': VK_F2,
        'F3': VK_F3,
        'F4': VK_F4,
        'F5': VK_F5,
        'F6': VK_F6,
        'F7': VK_F7,
        'F8': VK_F8,
        'F9': VK_F9,
        'F10': VK_F10,
        'F11': VK_F11,
        'F12': VK_F12
    }

    KEY_MAPPINGS = {
        '\n': VK_ENTER,
        '\b': VK_BACK_SPACE,
        '\t': VK_TAB,
        ' ' : VK_SPACE,
        ',' : VK_COMMA,
        '-' : VK_MINUS,
        '.' : VK_PERIOD,
        '/' : VK_SLASH,
        ';' : VK_SEMICOLON,
        '=' : VK_EQUALS,
        '[' : VK_OPEN_BRACKET,
        '\\': VK_BACK_SLASH,
        ']' : VK_CLOSE_BRACKET,
        '*' : VK_MULTIPLY,
        '+' : VK_ADD,
        '&' : VK_AMPERSAND,
        '<' : VK_LESS,
        '>' : VK_GREATER,
        '@' : VK_AT,
        '^' : VK_CIRCUMFLEX,
        '!' : VK_EXCLAMATION_MARK,
        '#' : VK_NUMBER_SIGN,
        '_' : VK_UNDERSCORE,
        "'" : VK_QUOTE
    }

    SHIFT_KEY_MAPPINGS = {
        '"': VK_QUOTE,
        '$': ord('4'),
        '(': ord('9'),
        ')': ord('0'),
        ':': VK_SEMICOLON
    }

    INPUT_PORT = 13246
    SERVER_PORT = 13246

    def __init__(self, ip):
        self._ip = ip
        self._output_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._input_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._input_socket.settimeout(2)
        self._input_socket.bind(('', AirHidDriver.INPUT_PORT))

    def close(self):
        self._output_socket.close()
        self._input_socket.close()

    def _listen_for_replies(self):
        try:
            data, addr = self._input_socket.recvfrom(1024)
            print "%s replied: %s" % (addr, data)
            return True
        except:
            return False

    def _send(self, data):
        print "sending: " + data
        self._output_socket.sendto(data, (self._ip, AirHidDriver.SERVER_PORT))

    def _vkey_to_airhid_button_code(self, vkey):
        if vkey in AirHidDriver.TRANSLATION_TABLE:
            return str(AirHidDriver.TRANSLATION_TABLE[vkey])
        else:
            return str(vkey)

    def _get_char_code(self, c):
        if c in string.ascii_lowercase:
            c = c.upper()
            return self._vkey_to_airhid_button_code(ord(c))
        elif c in string.ascii_uppercase:
            return self._vkey_to_airhid_button_code(ord(c)) + AirHidDriver.SHIFT
        elif c in AirHidDriver.KEY_MAPPINGS:
            return self._vkey_to_airhid_button_code(AirHidDriver.KEY_MAPPINGS[c])
        elif c in AirHidDriver.SHIFT_KEY_MAPPINGS:
            return self._vkey_to_airhid_button_code(AirHidDriver.SHIFT_KEY_MAPPINGS[c]) + AirHidDriver.SHIFT
        else:
            raise ValueError('Cannot encode character: %s' % c)

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
        self._send("url." + url)
        return self

    def typeText(self, text):
        format = "cmd."
        code = None
        for c in text:
            code = self._get_char_code(c)
            self._send(format + code)
            self._send(format + code + "_UP")
        return self

    def press_action_key(self, name, shift=False, ctrl=False, alt=False):
        if name not in AirHidDriver.ACTION_KEYS:
            raise ValueError('Unknown action key name: %s' % name)

        format = "cmd."
        command = str(AirHidDriver.ACTION_KEYS[name])
        if shift:
            command += AirHidDriver.SHIFT
        if ctrl:
            command += AirHidDriver.CTRL
        if alt:
            command += AirHidDriver.ALT
        self._send(format + command)
        return self

    def ping(self):
        format = "from:airhid"
        self._send(format)
        return self._listen_for_replies()
