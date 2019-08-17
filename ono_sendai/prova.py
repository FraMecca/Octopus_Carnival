from picotui.context import Context
from picotui.screen import Screen

from time import sleep

from widgets import *

class FrameFactory:
    titles = ['0x10', '0x11', '0x12', '0x13', '0x14', '0x15', '0x16', '0x17',
              '0x18', '0x19', '0x1A', '0x1B', '0x1D', '0x1E', '0x1F', '0x20',
              '0x21', '0x22', '0x23', '0x24', '0x25', '0x26', '0x27',
              '0x28', '0x29', '0x2A', '0x2B', '0x2D', '0x2E', '0x2F', '0x30'
              '0x31', '0x32', '0x33', '0x34', '0x35', '0x36', '0x37', '0x00'] # more than enough

    def __init__(self, d):
        self.np = 13
        self.d = d
        self.widgets = []
        self.x = 1 + self.np
        self.y = 1
        self.titlen = 0
        self.hand = None
        self.maxwidth = 0
    
    def newFrame(self, cards):
        # can handle 9 frames per row
        assert type(cards) is list, type(cards)

        h = 2 + len(cards) # height ?
        self.maxwidth = h if h > self.maxwidth else self.maxwidth
        title = self.titles[self.titlen]
        w = WCardRadioButton(cards)

        self.d.add(self.x, self.y, WColoredFrame(12, h, title))
        self.d.add(self.x+1, self.y+1, w)

        self.widgets.append(w)
        self.advance()

    def advance(self):
        self.x += self.np
        self.titlen+=1
        if self.x > self.np * 9:
            # second row
            self.y += self.maxwidth
            self.x = 1 + self.np  # first column for hand

    def emptyFrame(self):
        title = self.titles[-1]
        w = WCardRadioButton(['', ''])

        self.d.add(self.x, self.y, WColoredFrame(12, 4, title))
        self.d.add(self.x+1, self.y+1, w)

        self.widgets.append(w)
        self.advance()
        

    def newHandFrame(self, cards):
        assert type(cards) is list, type(cards)
        h = 27 # height ?
        self.d.add(1, 1, WColoredFrame(12, h, 'HAND', blue))
        w = WCardRadioButton([f'{Fore.BLUE}'+cards[0]] + cards[1:-1] + [cards[-1]+f'{Style.RESET_ALL}'], isHand=True)
        self.d.add(2, 2, w)
        self.hand = w

    def getChoices(self):
        src = (None, None); dst = None

        if self.widgets[0].choice == 0:
            dst = 'Empty'
        if self.hand.choice > 1:
            src = 'Hand', self.hand.choice-2

        for i, w in enumerate(self.widgets[1:]):
            if w.choice == 0:
                assert dst != 'Empty'
                dst = i
            elif w.choice > 1:
                assert src[0] != 'Hand'
                src = i, w.choice-2
        return src, dst
                

cc = ['asd', 'asd']
c = ['asd', 'asd']

import state
table = state.table
hand = state.hand

exit = False
while not exit:
    with Context():

        Screen.attr_color(C_WHITE, C_GREEN)
        Screen.cls()
        Screen.attr_reset()
        tableDialog = Dialog(1, 1,  120, 30)
        f = FrameFactory(tableDialog)

        #### BUTTONS ####
        buttonOk = WColoredButton(7, "SND", C_RED)
        tableDialog.add(108, 28, buttonOk)
        buttonOk.finish_dialog = ACTION_OK
        buttonRst = WColoredButton(7, "RST", C_RED)
        tableDialog.add(100, 28, buttonRst)
        buttonRst.finish_dialog = ACTION_OK
        buttonMov = WColoredButton(7, "MOV", C_BLUE)
        tableDialog.add(92, 28, buttonMov)
        buttonMov.finish_dialog = ACTION_OK
        buttonDraw = WColoredButton(7, "DRW", C_RED)
        tableDialog.add(84, 28, buttonDraw)
        buttonDraw.finish_dialog = ACTION_OK

        buttonAbort = WColoredButton(13, f'{Fore.BLACK}'+" ABRT "+f'{Style.RESET_ALL}', C_WHITE)
        tableDialog.add(4, 28, buttonAbort)
        buttonAbort.finish_dialog = ACTION_OK
        def doExit(w):
            global exit ; exit = True
        buttonAbort.on_click = doExit

        #### FRAMES ####
        f.emptyFrame()
        for cards in table.widget_repr():
            f.newFrame(cards)
        f.newHandFrame(hand.widget_repr())

        tableDialog.redraw()
        res = tableDialog.loop()
        if res == 1001 or res == 9: # or res == KEY_END or res == KEY_ESC: # 1001 is exit? # 9 is ctrl-c
            exit = True
        else:
            print(*f.getChoices())
            sleep(2)
            table, hand = state.update_table(table, hand, *f.getChoices())


print('TODO: sempre due scelte')
