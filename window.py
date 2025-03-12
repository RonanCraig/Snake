import curses, threading, time

def _keyListener(window, callback):
    while True:
        key = window.getch()
        if key != -1: 
            try:
                char = chr(key)  
                callback(char)
            except ValueError:
                pass  
        time.sleep(0.01)  

class Window:
    def __init__(self, size):
        self.windowSize = size
        self.gameWindow = curses.newwin(self.windowSize, self.windowSize * 2, 5, 5)
        self.gameWindow.border()
        self.gameWindow.nodelay(True)
        self.messageWindow = curses.newwin(3, self.windowSize * 2, 2, 5)
        curses.curs_set(False)
        self.input_thread = None

    def displayMessage(self, message):
        self.messageWindow.clear()
        self.messageWindow.addstr(1, (self.windowSize * 2 - len(message)) // 2, message, curses.A_BOLD)
        self.messageWindow.refresh()

    def clearMessage(self):
        self.messageWindow.clear()
        self.messageWindow.refresh()

    def draw(self, positions, character):
        for xy in positions:
            self.gameWindow.addch(xy[1], xy[0], character)

    def clear(self):
        self.gameWindow.erase()

    def render(self):
        self.gameWindow.border()
        self.gameWindow.refresh()

    def maxY(self):
        return self.gameWindow.getmaxyx()[0]
    
    def maxX(self):
        return self.gameWindow.getmaxyx()[1]
    
    def onInputReceived(self, callback):
        if self.input_thread is None:
            self.input_thread = threading.Thread(target=_keyListener, args=(self.gameWindow, callback), daemon=True)
            self.input_thread.start()