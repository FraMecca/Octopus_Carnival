from picotui.widgets import *
from picotui.defs import *
from colorama import Style, Fore

red  = f'{Fore.RED}'.encode('utf-8')
blue  = f'{Fore.BLUE}'.encode('utf-8')
green  = f'{Fore.GREEN}'.encode('utf-8')
white  = f'{Fore.WHITE}'.encode('utf-8')


class WColoredButton(WButton):
    color = C_GREEN

    def __init__(self, w, text, color):
        super().__init__(w, text)
        self.color = color

    def redraw(self):
        self.goto(self.x, self.y)
        if self.disabled:
            self.attr_color(C_WHITE, C_GRAY)
        else:
            self.attr_color(C_WHITE, self.color)
        self.wr(self.t.center(self.w))
        self.attr_reset()

    def handle_mouse(self, *args, **kwargs):
        r = super().handle_mouse(args, kwargs)
        self.on_click(self)
        return r

    def handle_key(self, inp):
        pass

    def on_click(self, *args, **kwargs):
        pass

class WColoredFrame(WFrame):
    color = None
    rst = f'{Style.RESET_ALL}'.encode('utf-8')
    def __init__(self, w, h, title="", color=white):
        title = color.decode('utf-8') + title + self.rst.decode('utf-8')
        super().__init__(w, h, title)
        self.color = color
    def handle_key(self, inp):
        pass

    def draw_box(self, left, top, width, height):
        # Use http://www.utf8-chartable.de/unicode-utf8-table.pl
        # for utf-8 pseudographic reference
        bottom = top + height - 1
        self.goto(left, top)
        # "┌"
        self.wr(self.color+b"\xe2\x94\x8c"+self.rst)
        # "─"
        hor = self.color+ b"\xe2\x94\x80" * (width - 2) +self.rst
        self.wr(hor)
        # "┐"
        self.wr(self.color + b"\xe2\x94\x90" + self.rst)

        self.goto(left, bottom)
        # "└"
        self.wr(self.color + b"\xe2\x94\x94" + self.rst)
        self.wr(hor)
        # "┘"
        self.wr(self.color + b"\xe2\x94\x98" + self.rst)

        top += 1
        while top < bottom:
            # "│"
            bar = self.color + b"\xe2\x94\x82" + self.rst
            self.goto(left, top)
            self.wr(bar)
            self.goto(left + width - 1, top)
            self.wr(bar)
            top += 1

class WCardRadioButton(WRadioButton):
    isHand = False

    def __init__(self, items, id, cb, isHand=False):
        super().__init__(items)
        self.choice = 1
        self.isHand = isHand
        self.cb = cb
        self.id = id

    def handle_key(self, inp):
        pass # TODO: maybe enable keyboard

    def redraw(self):
        i = 0
        if self.focus:
            self.attr_color(C_B_BLUE, None)
        for t in self.items:
            self.goto(self.x, self.y + i)
            self.wr("(*) " if self.choice == i and i > 1
                    else "[-] " if self.choice == 0 and i == 0 and not self.isHand
                    else "[ ] " if i == 0 and not self.isHand
                    else "( ) " if i > 1 else "    ")
            self.wr(t)
            i += 1
        self.attr_reset()

    def handle_mouse(self, x, y):
        newchoice = y - self.y
        self.choice = 1 if self.choice == newchoice else newchoice
        if self.choice != 1:
            self.cb(self.id)
        self.redraw()
        self.signal("changed")
