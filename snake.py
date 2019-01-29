import random
from copy import deepcopy
import pygame
from pygame.locals import *


class TheGame:
    """класс визуализации и процесса игры"""

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)
        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))


    def draw_snake(self, snake):
        for p, part in enumerate(snake.position):
            c = p * 7
            if 75 + c > 255:
                c = 255 - 75
            pygame.draw.rect(self.screen, pygame.Color(50 + c + 10* (-1)**(c // 7), c, 75 + c),
                                 (part[0] * self.cell_size, part[1] * self.cell_size, self.cell_size, self.cell_size))

    def draw_apple(self, apple):
        colors = [(154, 205, 50), (34, 139, 34), (205, 92, 92), (0, 250, 154), (0, 255, 0), (50, 205, 50)]

        pygame.draw.rect(self.screen, pygame.Color(colors[apple.colornum][0], colors[apple.colornum][1], colors[apple.colornum][2]),
                         (apple.position[0] * self.cell_size, apple.position[1] * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Snake')
        snake = Snake()
        apple = Apple()
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            self.screen.fill(pygame.Color('white'))
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if (ev.key == pygame.K_DOWN or ev.key == ord('s')) and snake.move != "UP":
                        snake.move = "DOWN"
                    elif (ev.key == pygame.K_LEFT or ev.key == ord('a')) and snake.move != "RIGHT":
                        snake.move = "LEFT"
                    elif (ev.key == pygame.K_RIGHT or ev.key == ord('d')) and snake.move != "LEFT":
                        snake.move = "RIGHT"
                    elif (ev.key == pygame.K_UP or ev.key == ord('w')) and snake.move != "DOWN":
                        snake.move = "UP"
            snake.update(apple)
            self.draw_apple(apple)
            self.draw_snake(snake)
            self.draw_grid()
            if not snake.alive():
                running = False
            pygame.display.flip()
            clock.tick(self.speed)
        print ('Score:', snake.len-5)
        pygame.quit()


class Snake:
    def __init__(self, move = 'RIGHT', position = [(4, 0), (3, 0), (2, 0), (1,0), (0,0)]):
        self.move = move
        self.position = position
        self.len = len(self.position)

    def update(self, apple):
        move = self.move
        end = self.position[-1]
        head = self.position[0]
        if move == 'LEFT':
            head = (head[0] - 1, head[1])
        elif move == 'RIGHT':
            head = (head[0] + 1, head[1])
        elif move == 'UP':
            head = (head[0], head[1] - 1)
        elif move == 'DOWN':
            head = (head[0], head[1] + 1)
        for part in range(len(self.position) - 1, 0, -1):
            self.position[part] = self.position[part - 1]
        self.position[0] = head
        if head == apple.position:
            self.position.append(end)
            apple.spawn(self.position)
        self.len = len(self.position)

    def alive(self):
        for part in range(1, len(self.position)):
            if self.position[part] == self.position[0]:
                return False
        if 0 <= self.position[0][0] < game.cell_width and 0<= self.position[0][1] < game.cell_height:
            return True
        return False


class Apple:
    def __init__(self, position = (5, 5), colornum = random.randint(0,5)):
        self.position = position
        self.colornum = colornum

    def spawn(self, snakeposition):
        self.position = (random.randint(0, game.cell_width - 1), random.randint(0, game.cell_height - 1))
        self.colornum = random.randint(0, 5)
        while snakeposition.count(self.position) == 1:
            self.position = (random.randint(0, game.cell_width - 1), random.randint(0, game.cell_height - 1))



if __name__ == '__main__':
    game = TheGame(600, 600, 20)
    game.run()

