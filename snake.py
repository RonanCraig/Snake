
import time, curses, random
from curses import wrapper

class Snake:
    def __init__(self):
        self.segments = [[1,4],[1,3],[1,2],[1,1]]
        self.direction = "down"

    def move(self):
        front = [self.segments[0][0], self.segments[0][1]]

        if self.direction == "up":
            front[1] = front[1] - 1
        if self.direction == "left":
            front[0] = front[0] - 1
        if self.direction == "down":
            front[1] = front[1] + 1
        if self.direction == "right":
            front[0] = front[0] + 1

        self.previousPos = self.segments.pop()
        self.segments.insert(0,front)

    def setDirection(self, direction):
        if direction == "left" and self.direction == "right":
            return
        elif direction == "right" and self.direction == "left":
            return
        elif direction == "up" and self.direction == "down":
            return
        elif direction == "down" and self.direction == "up":
            return
        self.direction = direction

    def grow(self):
        try:
            self.segments.append(self.previousPos)
        except any:
            pass

    def head(self):
        return self.segments[0]
    
class Window:
    def __init__(self):
        self.windowSize = 20
        self.gameWindow = curses.newwin(self.windowSize, self.windowSize*2, 5, 5)
        self.gameWindow.border()
        self.gameWindow.nodelay(True)
        self.messageWindow = curses.newwin(3, self.windowSize * 2, 2, 5)  
        curses.curs_set(False)

    def displayMessage(self, message):
        self.messageWindow.clear()
        self.messageWindow.addstr(1, (self.windowSize * 2 - len(message)) // 2, message, curses.A_BOLD)
        self.messageWindow.refresh()

    def clearMessage(self):
        self.messageWindow.clear()
        self.messageWindow.refresh()

    def draw(self, snake, food):
        self.gameWindow.clear()
        for xy in snake.segments:
            self.gameWindow.addch(xy[1], xy[0], 'x')
        for food in food:
            self.gameWindow.addch(food[1], food[0], 'o')
        self.gameWindow.border()
        self.gameWindow.refresh()

    def maxY(self):
        return self.gameWindow.getmaxyx()[0]
    
    def maxX(self):
        return self.gameWindow.getmaxyx()[1]

class Food:
    def __init__(self, maxX, maxY, excludedPositions):
        self.foodPositions = []  
        while len(self.foodPositions) < 3:
            self.generateNewFood(maxX, maxY, excludedPositions)

    def generateNewFood(self, maxX, maxY, excludedPositions):
        while(True):
            x = random.randint(1, maxX - 2)  
            y = random.randint(1, maxY - 2)

            if (x, y) not in self.foodPositions and [x, y] not in excludedPositions:
                self.foodPositions.append((x, y))
                break

    def removeFood(self, pos):
        self.foodPositions.remove(pos)

class Game:
    def __init__(self):
        self.delayInSeconds = 0.25
        self.window = Window()
        self.snake = Snake()
        self.food = Food(self.window.maxX(), self.window.maxY(), self.snake.segments)

    def run(self):
        while(True):
            self.getInput()
            self.update()
            time.sleep(self.delayInSeconds)

    def getInput(self):
        try:
            while True:  
                key = self.gameWindow.getkey()
                if key == 'w':
                    self.snake.setDirection("up")
                elif key == 'a':
                    self.snake.setDirection("left")
                elif key == 's':
                    self.snake.setDirection("down")
                elif key == 'd':
                    self.snake.setDirection("right")
        except curses.error:
            pass  

    def update(self):
        self.snake.move()

        if self.checkIsGameOver():
            self.endGame()
            return
            
        self.handleSnakeEat()
        self.window.draw(self.snake, self.foodPositions)

    def handleSnakeEat(self):
        snakeHead = self.snake.head()
        for food in self.food.foodPositions:
            if snakeHead[0] == food[0] and snakeHead[1] == food[1]:
                self.snake.grow()
                self.food.generateNewFood(self.window.maxX(), self.window.maxY(), self.snake.segments)
                self.food.removeFood(food)
                break
        
    def checkIsGameOver(self):
        snakeHead = self.snake.head()
        if snakeHead[0] <= 0 or snakeHead[1] <= 0 :
            return True
        elif snakeHead[0] >= self.window.maxX() - 1 :
            return True
        elif snakeHead[1] >= self.window.maxY() - 1 :
            return True
        elif snakeHead in self.snake.segments[1:] :
            return True
        return False

    def endGame(self):
        
        self.window.displayMessage("Game Over")
        self.draw(self.snake, self.foodPositions)
        time.sleep(3)

        self.window.clearMessage()
        self.snake = Snake()
        self.food = Food()

    



def main(stdscr):
    game = Game()
    game.run()

if __name__ == "__main__":
    wrapper(main)
