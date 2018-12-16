__author__ = 'tales.cpadua'
import pygame
import util
import copy
import time
import random


from gameobjects.snake import Snake
from gameobjects.fruit import Fruit


class Game():
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)

    def __init__(self, screen_width, screen_height, block_size):
        # init pygame
        pygame.init()

        self.game_over = False

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.block_size = block_size

        # set default font
        self.game_font = pygame.font.SysFont(None, 25)
        self.running = True

        # create display
        self.game_display = pygame.display.set_mode((self.screen_width, self.screen_height))

        # set clock for fps control
        self.clock = pygame.time.Clock()
        self.fps = 1

        # instantiate snake
        self.snake = Snake(self.game_display, self.block_size)

        # instantiate fruit
        self.fruit = Fruit(self.screen_width, self.screen_height, self.block_size)

        # set window name
        pygame.display.set_caption("Snake")

        #FOR BFS:
        self.solve_path = []

        self.new_game = True

    def main_loop(self):
        while self.running:
            # Handle game over situation
            if self.game_over:
                print("HIGEST LENGTH:"),
                print(len(self.snake.segments))
                self.game_over_dialog()

            ##!!!!: Them autoplay function vao day
            #print(self.new_game)
            if self.new_game:
                seg_list = self.snake.segments_list()
                start = time.time()
                self.bfs((seg_list[0], seg_list, self.snake.x_velocity, self.snake.y_velocity))
                #self.random((seg_list[0], seg_list, self.snake.x_velocity, self.snake.y_velocity))
                end = time.time()
                print("TIME:"),
                print(end - start)
            if len(self.solve_path) > 0:
                print("PATH"),
                print(self.solve_path)
                action = self.solve_path.pop(0)
                #print("PATH")
                #print(self.solve_path)
                #print(action)

                #auto play
                if action == "right":
                    self.snake.turn_right()
                elif action == "left":
                    self.snake.turn_left()
                elif action == "down":
                    self.snake.turn_down()
                elif action == "up":
                    self.snake.turn_up()

            if len(self.solve_path) == 0:
                self.new_game = True

            else:
                for event in pygame.event.get():
                    # Handle exit through x corner button
                    if event.type == pygame.QUIT:
                        self.running = False

                    """
                    # Handle KeyDown events. Note that it will works with arrows and WASD
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.snake.turn_left()
                            break
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.snake.turn_right()
                            break
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.snake.turn_up()
                            break
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.snake.turn_down()
                            break

                        # handle pause game
                        if event.key == pygame.K_ESCAPE:
                            self.pause_game()
                    """

            # execute snake logic
            self.snake.move()
            # Check collision with boundaries
            if self.check_collision():
                self.game_over = True

            #check if eated fruit
            if self.check_fruit_collision():
                self.snake.add_segment()
                self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
                self.new_game = True

            #first you draw, then you update to see changes
            self.game_display.fill(self.white)
            self.draw_fruit(self.fruit)
            self.draw_snake(self.snake)
            pygame.display.flip()
            #set fps
            self.clock.tick(self.fps)

    ###### bfs ######
    def random(self, state):
        successors = self.get_succesors(state)
        print("SUCC")
        print(successors)
        self.solve_path = random.choice(successors)
        self.new_game = True

    def bfs(self, state):
        print("----------------------------------------------")
        print("BFS")
        fringe = util.Queue()
        expanded = []
        fringe.push((state, []))
        total_succ = 0
        while not fringe.isEmpty():
            pop = fringe.pop()
            cur_state = pop[0]
            actions = pop[1]

            if cur_state in expanded:
                continue

            expanded.append(cur_state)

            if self.can_eat_food(cur_state):
                print("BINGO")
                self.solve_path = actions
                break

            successors = self.get_succesors(cur_state)
            #print("expanding...")
            total_succ += len(successors)
            for state, action in successors:
                fringe.push((state, actions + [action]))
        print("EXPANDED:"),
        print(total_succ)
        self.new_game = False

    def get_succesors(self, state):
        head_pos, segment_list, x_vel, y_vel = state
        pos_x, pos_y = head_pos
        successors = []
        for ((new_xvel, new_yvel), action) in [((-1*self.block_size,0),"left"), ((1*self.block_size,0),"right"), ((0,-1*self.block_size),"up"), ((0,1*self.block_size), "down")]:
            if (new_xvel*x_vel < 0) or (new_yvel*y_vel < 0):
                pass
            else:
                new_snake = self.move_virtual(head_pos, segment_list, new_xvel, new_yvel)
                ##print new_snake
                ##print self.is_collision(new_snake[0], new_snake[1][1:])
                if not self.is_collision(new_snake[0], new_snake[1][1:]):
                    successors.append((new_snake, action))
                    #print(successors)
        return successors

    def succ_num(self, state):
        return len(self.get_succesors)

    def move_virtual(self, head, body, x_vel, y_vel):
        """move virtual snake defined by head_pos and seg_list using x_vel and y_vel"""
        hx, hy = head
        next_x = hx + x_vel
        next_y = hy + y_vel
        new_head = (next_x, next_y)

        body_copy = copy.copy(body)
        body_copy.pop()
        body_copy.insert(0, (next_x, next_y))

        return (new_head, body_copy, x_vel, y_vel)

    ###### end bfs #######

    # Check whether the head position is at food position
    def can_eat_food(self, state):
        head_pos = state[0]
        pos_x, pos_y = head_pos
        return ((self.fruit.pos_y == pos_y) and (self.fruit.pos_x == pos_x))

    # letting snake_segment an empty list will ignore the self-collision check
    def is_collision(self, head_pos, snake_segment = list()):
        pos_x, pos_y = head_pos
        if pos_x < 0 or \
                pos_x > self.screen_width - self.snake.block_size:
            return True
        if pos_y < 0 or \
                pos_y > self.screen_height - self.snake.block_size:
            return True

        if len(snake_segment) <= 4:
            return False
        else:
            for (x,y) in snake_segment:
                if pos_x == x and pos_y == y:
                    return True
            return False
    ###########################################################################

    #this method checks collisions that result in game over
    def check_collision(self):
        if self.snake.segments[0].pos_x < 0 or \
                self.snake.segments[0].pos_x > self.screen_width - self.snake.block_size:
            return True
        if self.snake.segments[0].pos_y < 0 or \
                self.snake.segments[0].pos_y > self.screen_height - self.snake.block_size:
            return True

        #check collision of the snake with itself
        head_pos_x = self.snake.segments[0].pos_x
        head_pos_y = self.snake.segments[0].pos_y
        for s in self.snake.segments[1:]:
            if head_pos_x == s.pos_x and head_pos_y == s.pos_y:
                return True
        return False


    #Check if snake eats fruit
    def check_fruit_collision(self):
        if self.fruit.pos_y == self.snake.segments[0].pos_y and self.fruit.pos_x == self.snake.segments[0].pos_x:
            return True
        return False

    #method for input general messages
    def put_message(self, message):
        pause_text = self.game_font.render(message, True, self.red)
        self.game_display.blit(pause_text, [self.screen_width / 2, self.screen_height / 2])

    # separate method so we can display slightly left from previous method
    def game_over_message(self):
        message = "Game over, press ENTER/SPACE to continue or ESC to quit"
        pause_text = self.game_font.render(message, True, self.red)
        self.game_display.blit(pause_text, [self.screen_width / 5, self.screen_height / 2])

    # handle pause situation
    def pause_game(self):
        paused = True
        self.put_message("Game is Paused")
        pygame.display.update()
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
            self.clock.tick(30)

    # Handle game over situation
    def game_over_dialog(self):
        while self.game_over:
            self.game_display.fill(self.white)
            self.game_over_message()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.new_game = True
                        return
                    if event.key == pygame.K_ESCAPE:
                        self.exit_game()

    #Reset variables to a new game in case of playing again
    def reset_game(self):
        self.snake.reset_snake()
        self.game_over = False
        self.fruit.respawn(self.screen_width, self.screen_height, self.snake)
        pygame.display.flip()

    #draw snake segments
    def draw_snake(self, snake):
        for s in self.snake.segments:
            self.game_display.fill(self.snake.color, rect=[s.pos_x, s.pos_y, snake.block_size, snake.block_size])

    def draw_fruit(self, fruit):
        self.game_display.fill(self.red, rect=[fruit.pos_x, fruit.pos_y, fruit.block_size, fruit.block_size])

    def exit_game(self):
        pygame.quit()
        quit()
