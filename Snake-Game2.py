from tkinter import *
import random

# Making these variables constants, these variables won't be changed
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
SPEED = 40   # speed of the snake, how fast the game updates
SIZE = 20  # size of the food and body of the snake
BODY_PARTS = 2  # the snake starts the game off with two body parts
BACKGROUND_COLOR = "#324ea8" # the color is a type of blue
SNAKE_COLOR = "#FFFFFF"
FOOD_COLOR = "#000000"



class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []  # list of coordinates
        self.squares = []  # list of square graphics

        # Creating the list of coordinates so that the snake will appear at the top left corner
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Each square will be appended into the list
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y, x + SIZE, y + SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    # Food object
    def __init__(self):
# Allows for the food to spawn randomly in the available window size
        x = random.randint(0, (WINDOW_WIDTH/SIZE)-1) * SIZE
        y = random.randint(0, (WINDOW_HEIGHT / SIZE) - 1) * SIZE

        self.coordinates = [x,y]

        canvas.create_oval(x, y, x + SIZE, y + SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    # Unpacking the head of the snake
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SIZE
    elif direction == "down":
        y += SIZE
    elif direction == "left":
        x -= SIZE
    elif direction == "right":
        x += SIZE


    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SIZE, y + SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        score += 100

        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
# A body part of the snake will only delete if you don't run into a food object
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if collision(snake):
        gameOver()

    else:
# Calls the next turn function again
        win.after(SPEED, next_turn, snake, food)

def direction_change(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def collision(snake):
# Unpacking the head of the snake
    x, y = snake.coordinates[0]
# An if statement that ends the game when colliding with the game window borders
    if x < 0 or x >= WINDOW_WIDTH:
        return True

    elif y < 0 or y >= WINDOW_HEIGHT:
        return True

    for body_parts in snake.coordinates[1:]:
        if x == body_parts[0] and y == body_parts[1]:
            return True
    return False

def gameOver():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font =('Comic Sans Ms', 70), text="GAME OVER", fill="red", tag="gameover")

win = Tk()
win.title("Crazy Snake Game")
win.resizable(False, False) # Window cannot be resized

score = 0
direction = 'down'

label = Label(win, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(win, bg=BACKGROUND_COLOR, height=WINDOW_HEIGHT, width=WINDOW_WIDTH)
canvas.pack()

win.update()

win.bind('<Up>', lambda event: direction_change('up'))
win.bind('<Down>', lambda event: direction_change('down'))
win.bind('<Left>', lambda event: direction_change('left'))
win.bind('<Right>', lambda event: direction_change('right'))

# Objects
snake = Snake()
food = Food()

next_turn(snake, food)

win.mainloop()
