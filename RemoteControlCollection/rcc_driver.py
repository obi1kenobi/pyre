import socket
import string
from time import sleep

class RemoteControlCollectionDriver:

    RCC_ESC = "<esc>"
    RCC_TAB = "<tab>"
    RCC_UP = "<up>"
    RCC_DOWN = "<down>"
    RCC_LEFT = "<left>"
    RCC_RIGHT = "<right>"
    RCC_DEL = "<del>"
    RCC_BACKSPACE = "<Back>"
    RCC_SHIFT_DOWN = "<shift>down"
    RCC_SHIFT_UP = "<shift>up"
    RCC_ENTER = "<Enter>"
    RCC_CTRL_DOWN = "<ctrl>down"
    RCC_CTRL_UP = "<ctrl>up"
    RCC_ALT_DOWN = "<alt>down"
    RCC_ALT_UP = "<alt>up"
    RCC_WIN = "<win>"

    ACTION_KEYS = {
        'TAB': RCC_TAB,
        'ENTER': RCC_ENTER,
        'LEFT': RCC_LEFT,
        'UP': RCC_UP,
        'RIGHT': RCC_RIGHT,
        'DOWN': RCC_DOWN,
        'BACK_SPACE': RCC_BACKSPACE,
        'DELETE': RCC_DEL
    }

    KEY_MAPPINGS = {
        '\n': RCC_ENTER
    }


    def __init__(self, ip, udp_port, tcp_port):
        self._ip = ip
        self._socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._udp_port = udp_port
        self._tcp_port = tcp_port

        self._socket_tcp.connect((self._ip, self._tcp_port))
        self._socket_udp.setblocking(0)
        self._socket_tcp.setblocking(0)

    def _build_command(self, command, *args):
        prefix_bytes = [128, 21]

        bytes = prefix_bytes

        if command == "scroll":
            bytes.append(9)
        elif command == "right_click":
            print "command is r click"
            bytes.append(8)
        elif command == "left_click_down":
            bytes.append(5)
        elif command == "left_click_up":
            bytes.append(6)
        elif command == "mouse_start":
            bytes.append(0)
        elif command == "mouse_move":
            bytes.append(4)
        elif command == "mouse_release":
            bytes.append(1)
        elif command == "end_string":
            bytes = [128, 10]

        if args:
            bytes.extend(args)

        print bytes

        return bytearray(bytes)


    def _send(self, data, protocol="udp"):
        # print "sending: " + data

        if protocol == "udp":
            self._socket_udp.sendto(data, (self._ip, self._udp_port))
        else:
            self._socket_tcp.send(data)

    def _get_char_code(self, c):
        return RemoteControlCollectionDriver.KEY_MAPPINGS.get(c, c)

    def left_click(self):
        self._send(self._build_command("left_click_down"), protocol="tcp")
        self._send(self._build_command("left_click_up"))
        return self

    def right_click(self):
        self._send(self._build_command("right_click"))
        return self

    def scroll_up(self, ticks=1):
        self._send("[cmd_scroll]pageup", protocol="tcp")
        return self

    def scroll_down(self, ticks=1):
        self._send("[cmd_scroll]pagedown", protocol="tcp")
        return self

    def move_mouse(self, deltaX, deltaY):
        pivot_point = 128

        # Have to center a virtual phone swipe on the center value,
        # so we can move in any direction an equal amount
        center_mouse_command = self._build_command("mouse_start", pivot_point, pivot_point)

        # You can only send 1 byte for each deltaX, deltaY, so
        # if dX > 1 byte of movement, then we must repeat it
        x_times, x_pixels = divmod(deltaX, pivot_point)
        y_times, y_pixels = divmod(deltaY, pivot_point)

        x_sign = 1 if deltaX >= 0 else -1
        y_sign = 1 if deltaY >= 0 else -1

        # Limits of mouse motion per swipe, if dX, dY > 128
        x_movement_extrema = min(255, max(0, pivot_point + x_sign * pivot_point))
        y_movement_extrema = min(255, max(0, pivot_point + y_sign * pivot_point))

        for i in range(abs(x_times)):
            self._send(center_mouse_command)
            self._send(self._build_command("mouse_move", x_movement_extrema, pivot_point))
            sleep(0.05)

        for i in range(abs(y_times)):
            self._send(center_mouse_command)
            self._send(self._build_command("mouse_move", pivot_point, y_movement_extrema))
            sleep(0.05)

        # Any final offset
        self._send(center_mouse_command)
        self._send(self._build_command("mouse_move", pivot_point + x_sign * x_pixels, pivot_point + y_sign * y_pixels))

        return self

    def type(self, text):
        for c in text:
            self._send("[cmd_keyboard]%s" % self._get_char_code(c))
        
        # self._send(self._build_command("end_string"), protocol="tcp")

        return self

    def press_action_key(self, name, shift=False, ctrl=False, alt=False):
        pass
