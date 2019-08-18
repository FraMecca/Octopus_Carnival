from picotui.context import Context
from picotui.screen import Screen

from time import sleep
import os

from widgets import *
import state

action = ''
exit = False
ID = "tui"

game = state.State([ID, "bot1"])

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

    def constrainAllWidgets(self, callerId):
        cc = self.widgets[callerId].choice if id != -1 else self.hand.choice

        # check hand first
        if callerId != -1 and self.hand.choice > 1 and cc > 1:
            self.hand.choice = 1
            self.hand.redraw()
            return
        # check other widgets    
        for w in self.widgets:
            if w.id != callerId and w.choice != 1:
                if w.choice == 0 and cc == 0:
                    w.choice = 1
                    w.redraw()
                    return
                elif w.choice > 1 and cc > 1:
                    w.choice = 1
                    w.redraw()
                    return
                else:
                    pass
                
    def newFrame(self, cards):
        # can handle 9 frames per row
        assert type(cards) is list, type(cards)

        h = 2 + len(cards) # height ?
        self.maxwidth = h if h > self.maxwidth else self.maxwidth
        title = self.titles[self.titlen]
        w = WCardRadioButton(cards, len(self.widgets), self.constrainAllWidgets)

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
        w = WCardRadioButton(['', ''], len(self.widgets), self.constrainAllWidgets)

        self.d.add(self.x, self.y, WColoredFrame(12, 4, title))
        self.d.add(self.x+1, self.y+1, w)

        self.widgets.append(w)
        self.advance()
        

    def newHandFrame(self, cards):
        assert type(cards) is list, type(cards)
        h = 27 # height ?
        self.d.add(1, 1, WColoredFrame(12, h, 'HAND: '+str(len(cards)), blue)) 
        coloredCards = [f'{Fore.BLUE}'+cards[0]] + cards[1:-1] + [cards[-1]+f'{Style.RESET_ALL}']
        w = WCardRadioButton(coloredCards, -1, self.constrainAllWidgets, isHand=True)
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
                
def makeButtons(d):
    buttonSend = WColoredButton(7, "SND", C_RED)
    dialog.add(108, 28, buttonSend)
    buttonSend.finish_dialog = ACTION_OK
    def btnSend(w):
        global action; action = "SEND"
    buttonSend.on_click = btnSend

    buttonRst = WColoredButton(7, "RST", C_RED)
    dialog.add(100, 28, buttonRst)
    buttonRst.finish_dialog = ACTION_OK
    def btnReset(w):
        global action; action = "RESET"
    buttonRst.on_click = btnReset

    buttonMov = WColoredButton(7, "MOV", C_BLUE)
    dialog.add(92, 28, buttonMov)
    buttonMov.finish_dialog = ACTION_OK
    def btnMove(w):
        global action; action = "MOVE"
    buttonMov.on_click = btnMove

    buttonDraw = WColoredButton(7, "DRW", C_RED)
    dialog.add(84, 28, buttonDraw)
    buttonDraw.finish_dialog = ACTION_OK
    def btnDraw(w):
        global action; action = "DRAW"
    buttonDraw.on_click = btnDraw

    buttonAbort = WColoredButton(13, f'{Fore.BLACK}'+" ABRT "+f'{Style.RESET_ALL}', C_WHITE)
    dialog.add(4, 28, buttonAbort)
    buttonAbort.finish_dialog = ACTION_OK
    def doExit(w):
        global action ; action = "EXIT"
    buttonAbort.on_click = doExit

    buttonback = WColoredButton(7, " BAK ", C_MAGENTA)
    dialog.add(76, 28, buttonback)
    buttonback.finish_dialog = ACTION_OK
    def doBack(w):
        global action ; action = "BACK"
    buttonback.on_click = doBack

def wrong_play():
    from sys import stdout
    os.system('clear')
    print(f'{Fore.RED}'+'Wrong play. Retry...'+f'{Style.RESET_ALL}')
    sleep(2)

def make_auto_move():
    import sys
    from animation.octopus import animate
    pid = os.fork()
    if pid == 0:
        # child
        os.system('sleep 1')
        os.system('echo DRAW')
        sys.exit()
    else:
        p = os.waitpid(pid, os.WNOHANG)
        while p == (0, 0):
            animate(10)
            p = os.waitpid(pid, os.WNOHANG)
        game.draw()
        game.next_turn()
    

game.next_turn()
while not exit:
    while game.cur_player != ID:
        make_auto_move()
        
    table, hand = game.last()
    with Context():

        Screen.attr_color(C_WHITE, C_GREEN)
        Screen.cls()
        Screen.attr_reset()
        dialog = Dialog(1, 1,  120, 30)
        f = FrameFactory(dialog)

        makeButtons(dialog)

        #### FRAMES ####
        f.emptyFrame()
        for cards in table.widget_repr():
            f.newFrame(cards)
        f.newHandFrame(hand.widget_repr())

        dialog.redraw()
        res = dialog.loop()
        if res == 1001 or res == 9: # or res == KEY_END or res == KEY_ESC: # 1001 is exit? # 9 is ctrl-c
            exit = True
        else:
            if action == 'EXIT':
                exit = True
            elif action == 'MOVE':
                # TODO: transition effect
                game.advance(*f.getChoices()) # get them from next
            elif action == 'DRAW':
                game.draw()
                game.next_turn()
            elif action == 'RESET':
                while game.size() > 1:
                    game.backtrack()
            elif action == 'SEND':
                try:
                    game.done()
                    game.next_turn()
                except state.WrongMoveException as e:
                    wrong_play()
            elif action == 'BACK':
                game.backtrack()
            else:
                assert False
