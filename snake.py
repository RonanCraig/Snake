
import time, random
from window import windowWrapper
from window import Window
from inputManager import InputManager


class Snake:
    def __init__(self):
        self.segments = [[1,4],[1,3],[1,2],[1,1]]
        self.direction = "down"
        self.PPMode = False

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
        headX, headY = self.head()
        nextSegX, nextSegY = self.segments[1]
        if direction == "left" and headX == nextSegX + 1:
            return
        elif direction == "right" and headX == nextSegX - 1:
            return
        elif direction == "up" and headY == nextSegY + 1:
            return
        elif direction == "down" and headY == nextSegY - 1:
            return
        self.direction = direction

    def grow(self):
        try:
            self.segments.append(self.previousPos)
        except any:
            pass

    def head(self):
        return self.segments[0]
    
    def getChar(self, segment):
        if(self.PPMode is not True):
            return 'x'
        
        if(segment == self.segments[0]):
            return 'D'
        if(segment == self.segments[-1]):
            return '8'
        return '='
    
    def activatePPMode(self):
        self.PPMode = True
    
class Food:
    def __init__(self, maxX, maxY, excludedPositions):
        self.foodPositions = []  
        while len(self.foodPositions) < 5:
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
        self.window = Window(20)
        self.inputManager = InputManager(self.window)
        self.snake = Snake()
        self.food = Food(self.window.maxX(), self.window.maxY(), self.snake.segments)
        self.inputManager.onInputReceived(self.handleInput)
        self.inputManager.onWordRecieved("ppmode", lambda : self.snake.activatePPMode())
        self.score = 0
        self.bestScore = 0

    def run(self):
        while True:
            self.update()
            time.sleep(self.delayInSeconds)

            if(self.snake.direction == "up" or self.snake.direction == "down"): 
                time.sleep(self.delayInSeconds / 2)

    def handleInput(self, key):
        if key == 'w':
            self.snake.setDirection("up")
        elif key == 'a':
            self.snake.setDirection("left")
        elif key == 's':
            self.snake.setDirection("down")
        elif key == 'd':
            self.snake.setDirection("right")

    def update(self):
        self.snake.move()

        if self.checkIsGameOver():
            self.endGame()
            return
            
        self.handleSnakeEat()
        self.updateWindow()
        self.updateScoreText()

    def increaseSpeed(self):
        if(self.delayInSeconds <= 0.04):
            self.delayInSeconds = 0.04
            return

        self.delayInSeconds -= 0.005

    def updateScoreText(self):
        self.window.displayMessage("Score: " + str(self.score) + "      Best: " + str(self.bestScore))
        self.window.displayMessage(self.inputManager.getPreviousInputs())

    def handleSnakeEat(self):
        snakeHead = self.snake.head()
        for food in self.food.foodPositions:
            if snakeHead[0] == food[0] and snakeHead[1] == food[1]:
                self.snake.grow()
                self.food.generateNewFood(self.window.maxX(), self.window.maxY(), self.snake.segments)
                self.food.removeFood(food)
                self.score += 1
                self.increaseSpeed()
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
    
    def updateWindow(self):
        self.window.clear()

        for segment in self.snake.segments:
            self.window.draw(segment, self.snake.getChar(segment))

        self.window.draw(self.food.foodPositions, 'o')
        self.window.render()

    def endGame(self):
        
        self.window.displayMessage("Game Over")
        self.updateWindow()

        if self.score > self.bestScore:
            self.bestScore = self.score
        
        self.score = 0
        self.delayInSeconds = 0.25

        time.sleep(1.5)

        self.window.clearMessage()
        self.snake = Snake()
        self.food = Food(self.window.maxX(), self.window.maxY(), self.snake.segments)


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    windowWrapper(main)
