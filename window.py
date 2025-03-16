import curses
from curses import wrapper

class Window:
    def __init__(self, size):
        curses.initscr()
        self.windowSize = size
        self.gameWindow = curses.newwin(self.windowSize, self.windowSize * 2, 5, 5)
        self.gameWindow.border()
        self.gameWindow.nodelay(True)
        self.messageWindow = curses.newwin(3, self.windowSize * 2, 2, 5)
        curses.curs_set(False)
        self.render()

    def displayMessage(self, message):
        self.messageWindow.clear()
        self.messageWindow.addstr(1, (self.windowSize * 2 - len(message)) // 2, message, curses.A_BOLD)
        self.messageWindow.refresh()

    def clearMessage(self):
        self.messageWindow.clear()
        self.messageWindow.refresh()

    def draw(self, positions, character):
        if isinstance(positions[0], (list, tuple)):  
            for xy in positions:
                self.gameWindow.addch(xy[1], xy[0], character)
        else:  
            self.gameWindow.addch(positions[1], positions[0], character)

    def clear(self):
        self.gameWindow.erase()

    def render(self):
        self.gameWindow.border()
        self.gameWindow.refresh()

    def maxY(self):
        return self.gameWindow.getmaxyx()[0]
    
    def maxX(self):
        return self.gameWindow.getmaxyx()[1]
    
    def getch(self):
        return self.gameWindow.getch()


def windowWrapper(func):
    try:
        curses.wrapper(lambda stdscr: func())
    except KeyboardInterrupt:
        curses.curs_set(True)  
        