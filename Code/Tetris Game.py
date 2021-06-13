import pygame
import random

# A Tetris game application
__author__ = 'Michael Khoshahang'

# Global variables
screen_width = 800
screen_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height
pygame.font.init()
pygame.mixer.init()

# Shape Formats
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Shape(object):
    # A class of a piece object
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_shape(self, shape):
        self.shape = shape

    def set_color(self, color):
        self.color = color

    def set_rotation(self, rotation):
        self.rotation = rotation

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_shape(self):
        return self.shape

    def get_color(self):
        return self.color

    def get_rotation(self):
        return self.rotation

def get_shape():
    """
    The function return a random shape object.
    :return: a random shape object
    :rtype: object
    """
    return Shape(5, 0, random.choice(shapes))


def convert_shape_format(shape):
    """
    The function converts the shape format using the given shape
    :param shape: the shape to convert
    :return: list of the shape format
    :rtype: list
    """
    positions = list()
    format = shape.get_shape()[shape.get_rotation() % len(shape.get_shape())]  # getting the current shape according to the rotation

    for i, line in enumerate(format):
        for j, column in enumerate(list(line)):
            if column == '0':
                positions.append((shape.get_x() + j, shape.get_y() + i))

    for i, position in enumerate(positions):
        positions[i] = (position[0] - 2, position[1] - 4)

    return positions


def in_valid_space(shape, grid):
    """
    The function return True or False according to the validation of the given shape's space
    :param shape: the shape
    :param grid: the grid
    :return: True or False according to whether the shape's space is valid or not
    :rtype: bool
    """
    valid_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    valid_positions = [j for sub in valid_positions for j in sub]

    formatted = convert_shape_format(shape)
    for position in formatted:
        if position not in valid_positions:
            if position[1] > -1:
                return False
    return True


def update_score(new_score):
    """
    The function gets a new score and updates the max score if the new score is bigger then the previous score
    :param new_score: the new score
    :return: None
    """
    try:
        with open('Scores', 'x'):
            pass
        with open('Scores', 'w') as file:
            file.write('0')
    except:
        pass

    with open('Scores', 'r') as file:
        lines = file.readlines()
        score = lines[0].strip()

    with open('Scores', 'w') as file:
        if int(score) > new_score:
            file.write(str(score))
        else:
            file.write(str(new_score))


def get_max_score():
    """
    The function returns the max score from the Scores file
    :return: the max score
    :rtype: str
    """
    try:
        with open('Scores', 'x'):
            pass
        with open('Scores', 'w') as file:
            file.write('0')
    except:
        pass
    with open('Scores', 'r') as file:
        return file.readlines()[0].strip()


def has_lost(positions):
    """
    The function checks whether the play has lost the game or not
    :param positions: the positions of all the shapes on the screen
    :return: True or False according to whether the play has lost the game or not
    :rtype: bool
    """
    for position in positions:
        x, y = position
        if y < 1:
            return True
    return False


def display_text(surface, text, size, color):
    """
    The function displays text in the middle of the game screen
    :param surface: the Tetris game's screen
    :param text: the text to display
    :param size: the size of the text
    :param color: the color of the text
    :return:
    """
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width / 3 - label.get_width() / 2, top_left_y + play_height / 2 - label.get_height() / 2))


def clear_row(grid, locked_positions):
    """
    The function clears an entire row that was fully filled by shapes and shifts all the shapes
    :param grid: the grid of the game
    :param locked_positions: the locked positions of the shapes
    :return: the number of the cleared rows
    :rtype: int
    """
    cleared_rows = 0
    for i in range(len(grid)-1, -1, -1):
        if (0, 0, 0) not in grid[i]:
            cleared_rows += 1
            index = i
            for j in range(len(grid[i])):
                try:
                    del locked_positions[(j, i)]  # delete the row
                except:
                    pass
    if cleared_rows > 0:  # shifting all the shapes
        for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < index:
                locked_positions[(x, y + cleared_rows)] = locked_positions.pop(key)  # rewriting the locked positions
    return cleared_rows


def display_next_shape(next_shape, surface):
    """
    The function displays the next shape on the surface
    :param next_shape: the next shape
    :param surface: the Tetris game's screen
    :return: None
    """
    font = pygame.font.SysFont('comicsans', 30)
    next_shape_label = font.render('Next Shape:', 1, (255, 255, 255))
    surface.blit(next_shape_label, (top_left_x + play_width + 70, top_left_y + (play_height / 2) - 125))
    format = next_shape.get_shape()[next_shape.get_rotation() % len(next_shape.get_shape())]  # getting the current shape according to the rotation

    for i, line in enumerate(format):
        for j, column in enumerate(list(line)):
            if column == '0':
                pygame.draw.rect(surface, next_shape.get_color(), (top_left_x + play_width + 50 + j * block_size, top_left_y + play_height / 2 - 100 + i * block_size, block_size, block_size), 0)


def initialize_grid(locked_positions={}):
    """
    The function creates the grid of the Tetris game's screen
    :param locked_positions: the initialized locked positions (default empty dict)
    :return: the grid list
    :rtype: list
    """
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                grid[i][j] = locked_positions[(j, i)]
    return grid


def display_grid(surface, grid):
    """
    The function draws the grid on the surface
    :param surface: the Tetris game's screen
    :param grid: the grid to be drawn
    :return: None
    """

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + i*block_size), (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))


def display_screen(surface, grid, score=0, max_score=0):
    """
    The function displays the windows of the Tetris game
    :param surface: the Tetris game's screen
    :param grid: the grid of the Tetris game
    :param score: the player's score (default is 0)
    :param max_score: the player's highest score
    :return: None
    """
    surface.fill((0, 0, 0))
    pygame.font.init()
    title_label = pygame.font.SysFont('comicsans', 60).render('Tetris', 1, (255, 255, 255))
    surface.blit(title_label, (top_left_x + play_width / 2 - title_label.get_width() + 50, 30))

    score_label = pygame.font.SysFont('comicsans', 30).render(f'Score: {score}', 1, (255, 255, 255))
    surface.blit(score_label, (top_left_x + play_width + 90, top_left_y + play_height / 2 + 50))

    max_score_label = pygame.font.SysFont('comicsans', 30).render(f'Highest Score: {get_max_score()}', 1, (255, 255, 255))
    surface.blit(max_score_label, (top_left_x - 200, top_left_y + 360))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    display_grid(surface, grid)


def main(window):
    """
    The main function of the Tetris game
    :param window: the surface of the game
    :return: None
    """
    locked_positions = {}
    grid = initialize_grid(locked_positions)
    change_piece = False
    playing = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while playing:
        grid = initialize_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.set_y(current_piece.get_y() + 1)
            if not (in_valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.set_y(current_piece.get_y() - 1)
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                update_score(score)
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.set_x(current_piece.get_x() - 1)
                    if not in_valid_space(current_piece, grid):
                        current_piece.set_x(current_piece.get_x() + 1)
                if event.key == pygame.K_RIGHT:
                    current_piece.set_x(current_piece.get_x() + 1)
                    if not in_valid_space(current_piece, grid):
                        current_piece.set_x(current_piece.get_x() - 1)
                if event.key == pygame.K_DOWN:
                    current_piece.set_y(current_piece.get_y() + 1)
                    if not in_valid_space(current_piece, grid):
                        current_piece.set_y(current_piece.get_y() - 1)
                if event.key == pygame.K_UP:
                    current_piece.set_rotation(current_piece.get_rotation() + 1)
                    if not in_valid_space(current_piece, grid):
                        current_piece.set_rotation(current_piece.get_rotation() - 1)

        shape_position = convert_shape_format(current_piece)
        for i in range(len(shape_position)):
            x, y = shape_position[i]
            if y > -1:
                grid[y][x] = current_piece.get_color()

        if change_piece:
            for pos in shape_position:
                locked_positions[(pos[0], pos[1])] = current_piece.get_color()
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_row(grid, locked_positions) * 10
        try:
            display_screen(window, grid, score)
            display_next_shape(next_piece, window)  # displaying the next shape
            pygame.display.update()
        except:
            pass

        if has_lost(locked_positions):
            display_text(window, 'You Lost!', 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            playing = False
            update_score(score)
            pygame.mixer.music.stop()

    pygame.display.quit()


def main_menu():
    """
    The function displays the instruction of the game
    :return: None
    """
    window = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_icon(pygame.image.load('Tetris Icon.png'))
    display = True
    while display:
        window.fill((0, 0, 0))
        display_text(window, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display = False
                pygame.mixer.music.stop()
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.load("Tetris Theme Song.mp3")
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play()
                main(window)
                display = False
                pygame.mixer.music.stop()

    pygame.display.quit()


if __name__ == '__main__':
    pygame.display.set_caption('Tetris Game')
    main_menu()
