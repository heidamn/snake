import sys
import random
from copy import deepcopy
import pygame
from pygame.locals import *


class TheGame:
    """класс визуализации и процесса игры"""

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 100, difficulty: str = 'Normal', mode: str = 'AI') -> None:
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
        # Сложность игры (Easy/Normal)
        self.difficulty = difficulty
        # Количество пользователей (AI/1player/2players)
        self.mode = mode

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_snake(self, snake, *args):
        if len(args):
            if args[0] == 1:

                for p, part in enumerate(snake.position):
                    r = p % 2 + 2
                    b = p * 4
                    if 85 + b > 255:
                        b = 255 - 85
                    pygame.draw.rect(self.screen, pygame.Color(b, 50 + b + 20 * (-1) ** (r), 85 + b),
                                     (part[0] * self.cell_size, part[1] * self.cell_size, self.cell_size,
                                      self.cell_size))
            elif args[0] == 2:
                for p, part in enumerate(snake.position):
                    r = p % 2 + 2
                    b = p * 4
                    if 85 + b > 255:
                        b = 255 - 85
                    pygame.draw.rect(self.screen, pygame.Color(85 + b, b, 50 + b + 20 * (-1) ** (r)),
                                     (part[0] * self.cell_size, part[1] * self.cell_size, self.cell_size,
                                      self.cell_size))
        else:
            for p, part in enumerate(snake.position):
                r = p % 2 + 2
                b = p * 4
                if 85 + b > 255:
                    b = 255 - 85
                pygame.draw.rect(self.screen, pygame.Color(50 + b + 20 * (-1) ** (r), b, 85 + b),
                                     (part[0] * self.cell_size, part[1] * self.cell_size, self.cell_size, self.cell_size))

    def draw_apple(self, apple):
        colors = [(154, 205, 50), (34, 139, 34), (205, 92, 92), (0, 250, 154), (0, 255, 0), (50, 205, 50)]

        pygame.draw.rect(self.screen, pygame.Color(colors[apple.colornum][0], colors[apple.colornum][1], colors[apple.colornum][2]),
                         (apple.position[0] * self.cell_size, apple.position[1] * self.cell_size, self.cell_size, self.cell_size))

    def leaderboard(self, score):
        try:
            file = open("Score.txt").read()
        except:
            print('Input your name:')
            name = input()
            newfile = '1 ' + name.upper() + ' ' + str(score) + '\n'
            for i in range(2, 11):
                newfile += '{} EMPTY 0\n'.format(i)
            print(newfile)
            file = open("Score.txt", "w")
            file.write(newfile)
            file.close()
        else:
            positions = file.split('\n')
            positions = positions[0:-1]
            for place, position in enumerate(positions):
                position = position.split(' ')
                position[0], position[2] = int(position[0]), int(position[2])
                positions[place] = position
            for place, position in enumerate(positions):
                if position[2] < score:
                    print('Input your name:')
                    name = input()
                    positions.insert(place, [place, name.upper(), score])
                    pl = place
                    break
            else:
                print(file)
                return None
            for place in range(pl, len(positions)):
                positions[place][0] += 1
            newfile = ''
            for place in range(10):
                line = str(positions[place][0]) + ' ' + positions[place][1] + ' ' + str(positions[place][2])
                newfile += line + '\n'
            print(newfile)
            file = open("Score.txt", "w")
            file.write(newfile)
            file.close()

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Snake')
        if self.mode == '1player' or self.mode == 'AI':
            snake = Snake()
        elif self.mode == '2players':
            snake1 = Snake()
            snake2 = Snake(move='LEFT', position=[(self.cell_width - 5, self.cell_height - 1), (self.cell_width - 4, self.cell_height - 1), (self.cell_width - 3, self.cell_height - 1), (self.cell_width - 2, self.cell_height - 1), (self.cell_width - 1, self.cell_height - 1)])
        apple = Apple()
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            self.screen.fill(pygame.Color('white'))
            # управление
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if self.mode == '1player':
                        if (ev.key == pygame.K_DOWN or ev.key == ord('s')) and snake.move != "UP":
                            snake.move = "DOWN"
                        elif (ev.key == pygame.K_LEFT or ev.key == ord('a')) and snake.move != "RIGHT":
                            snake.move = "LEFT"
                        elif (ev.key == pygame.K_RIGHT or ev.key == ord('d')) and snake.move != "LEFT":
                            snake.move = "RIGHT"
                        elif (ev.key == pygame.K_UP or ev.key == ord('w')) and snake.move != "DOWN":
                            snake.move = "UP"
                    elif self.mode == '2players':
                        #snake 1
                        if ev.key == ord('s') and snake1.move != "UP":
                            snake1.move = "DOWN"
                        elif ev.key == ord('a') and snake1.move != "RIGHT":
                            snake1.move = "LEFT"
                        elif ev.key == ord('d') and snake1.move != "LEFT":
                            snake1.move = "RIGHT"
                        elif ev.key == ord('w') and snake1.move != "DOWN":
                            snake1.move = "UP"
                        #snake2
                        if ev.key == pygame.K_DOWN and snake2.move != "UP":
                            snake2.move = "DOWN"
                        elif ev.key == pygame.K_LEFT and snake2.move != "RIGHT":
                            snake2.move = "LEFT"
                        elif ev.key == pygame.K_RIGHT and snake2.move != "LEFT":
                            snake2.move = "RIGHT"
                        elif ev.key == pygame.K_UP and snake2.move != "DOWN":
                            snake2.move = "UP"
            if self.mode == "AI":
                snake.think(apple.position)
            if self.mode == '1player' or self.mode == 'AI':
                snake.update(apple, self.difficulty)
                self.draw_snake(snake)
            elif self.mode == '2players':
                snake1.update(apple, self.difficulty)
                snake2.update(apple, self.difficulty)
                self.draw_snake(snake1, 1)
                self.draw_snake(snake2, 2)
            self.draw_apple(apple)
            self.draw_grid()
            if self.mode == '1player' or self.mode == 'AI':
                if not snake.alive():
                    running = False
            elif self.mode == '2players':
                if not snake1.alive(snake2) and not snake2.alive(snake1):
                    running = False
                if not snake1.alive(snake2):
                    snake1.death()
                if not snake2.alive(snake1):
                    snake2.death()

            pygame.display.flip()
            clock.tick(self.speed)
        if self.mode == '1player' or self.mode == 'AI':
            print('Score:', snake.len-5)
            print('Difficulty:', self.difficulty)
            self.leaderboard(snake.len - 5)

        pygame.quit()


class Snake:
    def __init__(self, move='RIGHT', position=[(4, 0), (3, 0), (2, 0), (1, 0), (0, 0)]):
        self.move = move
        self.position = position
        self.len = len(self.position)

    def think(self, applepos):
        if self.position[0][0] == game.cell_width - 1:
            if self.move == 'DOWN':
                self.move = 'LEFT'
            else:
                self.move = 'DOWN'
        if self.position[0][0] == 1 and self.position[0][1] != 0 and self.position[0][1] != game.cell_height - 1:
            if self.position[0][1] > applepos[1]:
                self.move = 'LEFT'
            elif self.move == 'DOWN':
                self.move = 'RIGHT'
            else:
                self.move = 'DOWN'

        if self.position[0][0] == 0:
            if self.position[0][1] == 0:
                self.move = 'RIGHT'
            else:
                self.move = 'UP'

    def update(self, apple, difficulty):
        if self.position:
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
            if difficulty == "Easy":
                if head[0] < 0:
                    head = (game.cell_width - 1, head[1])
                elif head[0] == game.cell_width:
                    head = (0, head[1])
                if head[1] < 0:
                    head = (head[0], game.cell_height - 1)
                elif head[1] == game.cell_height:
                    head = (head[0], 0)
            self.position[0] = head
            if head == apple.position:
                self.position.append(end)
                apple.spawn(self.position)
            self.len = len(self.position)

    def alive(self, *args):
        if self.position:
            for part in range(1, len(self.position)):
                if self.position[part] == self.position[0]:
                    return False
            if len(args) == 1:
                othersnake = args[0]
                for part in othersnake.position:
                    if part == self.position[0]:
                        return False
            if 0 <= self.position[0][0] < game.cell_width and 0 <= self.position[0][1] < game.cell_height:
                return True
            return False
        return False

    def death(self):
        self.position=[]


class Apple:
    def __init__(self, position=(5, 5), colornum=random.randint(0, 5)):
        self.position = position
        self.colornum = colornum

    def spawn(self, snakeposition):
        self.position = (random.randint(0, game.cell_width - 1), random.randint(0, game.cell_height - 1))
        self.colornum = random.randint(0, 5)
        while snakeposition.count(self.position) == 1:
            self.position = (random.randint(0, game.cell_width - 1), random.randint(0, game.cell_height - 1))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        game = TheGame(400, 500, 20, difficulty=sys.argv[1])
    else:
        game = TheGame(400, 400, 20)
    game.run()
