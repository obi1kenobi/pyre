## Superclass for all exploit drivers, all drivers must implement these functions
## To work with the known exploits
class driver:
    def __init__(self, ip):
        raise NotImplementedError

    def left_click(self):
        raise NotImplementedError

    def right_click(self):
        raise NotImplementedError

    def move_mouse(self, deltaX, deltaY):
        raise NotImplementedError

    def typeText(self, text):
        raise NotImplementedError

    ## Action key names:
    ## 'TAB','ENTER','ESCAPE','PAGE_UP','PAGE_DOWN',
    ## 'END','HOME','LEFT','UP','RIGHT','DOWN','BACK_SPACE',
    ## 'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',
    ## 'CONTROL','ALT','SHIFT'
    def press_action_key(self, name, shift=False, ctrl=False, alt=False):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
