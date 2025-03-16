import threading, time

class InputManager:
    def __init__(self, window):
        self._window = window
        self.previousInputs = ""
        self.wordsAndCallbacks = []
        self.input_thread = None


    def onInputReceived(self, callback):
        self.callback = callback

        if self.input_thread is not None:
            return
        
        self.input_thread = threading.Thread(target=_keyListener, args=(self._window, self._handleInputRecieved), daemon=True)
        self.input_thread.start()

    def onWordRecieved(self, word, callback):
        if(len(word) > 10):
            raise ValueError("Word is too long")
        self.wordsAndCallbacks.append((word, callback))

    def getPreviousInputs(self):
        return self.previousInputs

    def _handleInputRecieved(self, c):
        if(len(self.previousInputs) > 10):
            self.previousInputs = self.previousInputs[1:]

        self.previousInputs += c
        for word, callback in self.wordsAndCallbacks:
            if self.previousInputs.endswith(word):
                callback()
                self.previousInputs = ""
            
        self.callback(c)

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