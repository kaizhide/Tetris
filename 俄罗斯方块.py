import pygame
import random

# 游戏区域大小

WINDOW_WIDTH = 800

WINDOW_HEIGHT = 600

CELL_SIZE = 30

# 方块类型及其形状

SHAPES = [

   [[1, 1, 1, 1]],

   [[1, 1], [1, 1]],

   [[1, 1, 0], [0, 1, 1]],

   [[0, 1, 1], [1, 1, 0]],

   [[1, 1, 1], [0, 0, 1]],

   [[1, 1, 1], [1, 0, 0]],

   [[1, 1, 1], [0, 1, 0]]
]

# 方块颜色

COLORS = [

   (0, 0, 0),

   (255, 0, 0),

   (0, 255, 0),

   (0, 0, 255),

   (255, 255, 0),

   (255, 0, 255),

   (0, 255, 255)
]

def draw_cell(screen, x, y, color):

   pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_shape(screen, shape, x, y, color):

   for i in range(len(shape)):

       for j in range(len(shape[i])):

           if shape[i][j] == 1:

               draw_cell(screen, x + j, y + i, color)


def check_collision(board, shape, x, y):

   for i in range(len(shape)):

       for j in range(len(shape[i])):

           if shape[i][j] == 1:

               if x + j < 0 or x + j >= len(board[0]) or y + i >= len(board) or board[y + i][x + j] != 0:

                   return True
   return False

def merge_shape(board, shape, x, y):

   for i in range(len(shape)):

       for j in range(len(shape[i])):

           if shape[i][j] == 1:

               board[y + i][x + j] = 1


def remove_completed_lines(board):

   completed_lines = []

   for i in range(len(board)):

       if all(board[i]):

           completed_lines.append(i)

   for line in completed_lines:

       del board[line]

       board.insert(0, [0] * len(board[0]))


def rotate_shape(shape):

   return list(zip(*reversed(shape)))


def main():

   pygame.init()

   screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

   clock = pygame.time.Clock()


   board_width = WINDOW_WIDTH // CELL_SIZE

   board_height = WINDOW_HEIGHT // CELL_SIZE


   board = [[0] * board_width for _ in range(board_height)]


   current_shape = random.choice(SHAPES)

   current_color = random.choice(COLORS)

   current_x = board_width // 2 - len(current_shape[0]) // 2

   current_y = 0


   game_over = False


   while not game_over:

       for event in pygame.event.get():

           if event.type == pygame.QUIT:

               game_over = True

           elif event.type == pygame.KEYDOWN:

               if event.key == pygame.K_LEFT:

                   if not check_collision(board, current_shape, current_x - 1, current_y):

                       current_x -= 1

               elif event.key == pygame.K_RIGHT:

                   if not check_collision(board, current_shape, current_x + 1, current_y):

                       current_x += 1

               elif event.key == pygame.K_DOWN:

                   if not check_collision(board, current_shape, current_x, current_y + 1):

                       current_y += 1

               elif event.key == pygame.K_UP:

                   rotated_shape = rotate_shape(current_shape)

                   if not check_collision(board, rotated_shape, current_x, current_y):

                       current_shape = rotated_shape


       if not check_collision(board, current_shape, current_x, current_y + 1):

           current_y += 1

       else:

           merge_shape(board, current_shape, current_x, current_y)

           remove_completed_lines(board)

           current_shape = random.choice(SHAPES)

           current_color = random.choice(COLORS)

           current_x = board_width // 2 - len(current_shape[0]) // 2

           current_y = 0

           if check_collision(board, current_shape, current_x, current_y):

               game_over = True

       screen.fill((255, 255, 255))

       for i in range(len(board)):

           for j in range(len(board[i])):

               if board[i][j] == 1:

                   draw_cell(screen, j, i, (0, 0, 0))

       draw_shape(screen, current_shape, current_x, current_y, current_color)

       pygame.display.flip()

       clock.tick(10)

   pygame.quiet()

if __name__ == '__main__':

   main()
