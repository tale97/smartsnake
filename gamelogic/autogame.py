import pygame
import time
import tests


from gameobjects.snake import Snake
from gameobjects.fruit import Fruit, FruitRand


class Game():
    red = (255, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)

    def __init__(self, screen_width, screen_height, block_size, fruitlist = ["rand"]):
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
        self.fps = 20
        # instantiate snake
        self.snake = Snake(self.game_display, self.block_size)

        # instantiate fruit
        if fruitlist == ["rand"]:
            self.fruit = FruitRand(self.screen_width, self.screen_height, self.block_size)
        else:
            self.fruit = Fruit(self.screen_width, self.screen_height, self.block_size, fruitlist)

        # set window name
        pygame.display.set_caption("Snake")

        self.total_path_length = 0

    def main_loop(self, agent, speed):
        self.fps = speed
        log_game = tests.GameLogger(agent.return_agent_name())
        #takes in agent as an input
        while self.running:

            # Handle game over situation
            if self.game_over:
                print("---------RESULT----------")
                print("Total path length:"),
                print(self.total_path_length)
                print("Total states expanded:"),
                print(agent.succesor_count)

                snake_length = len(self.snake.segments)
                log_game.record_snake_length(snake_length)
                log_game.normal_game_end()
                self.game_over_dialog()

            if agent.new_game:
                food_pos = (self.fruit.pos_x, self.fruit.pos_y)
                seg_list = self.snake.segments_list()

                # if using IDS agent, add depth to argument
                log_game.start_timer()
                if agent.return_agent_name() == "IDS":
                    state_with_depth = (seg_list[0], seg_list, self.snake.x_velocity, self.snake.y_velocity, 0)
                    print("________________________________________________" + str(agent.return_agent_name()))
                    agent.getpath(state_with_depth, food_pos, 0)
                else:
                    state = (seg_list[0], seg_list, self.snake.x_velocity, self.snake.y_velocity)
                    print("________________________________________________"+ str(agent.return_agent_name()))
                    agent.getpath(state, food_pos)

                path_length = len(agent.solve_path)
                self.total_path_length += path_length

                # Check if agent want to end game
                if agent.end_game:
                    log_game.record_get_path_time()
                    log_game.record_succesor_count(agent.succesor_count)
                    log_game.record_path(path_length)
                    self.game_over = True

                elif agent.found_food:
                    log_game.record_get_path_time()

                else:
                    print("Path to food not found :(")
                    log_game.record_get_path_time()

            if len(agent.solve_path) > 0:
                action = agent.solve_path.pop(0)
                if action == "right":
                    self.snake.turn_right()
                elif action == "left":
                    self.snake.turn_left()
                elif action == "down":
                    self.snake.turn_down()
                elif action == "up":
                    self.snake.turn_up()

            if len(agent.solve_path) == 0:
                agent.new_game = True

            else:
                for event in pygame.event.get():
                    # Handle exit through x corner button
                    if event.type == pygame.QUIT:
                        self.running = False
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
                #mark total successors count
                log_game.record_succesor_count(agent.succesor_count)
                print("Move " + str(path_length) + " squares")
                log_game.record_path(path_length)
                log_game.record_eat_fruit_time()

            #first you draw, then you update to see changes
            self.game_display.fill(self.white)
            self.draw_fruit(self.fruit)
            self.draw_snake(self.snake)
            pygame.display.flip()
            #set fps
            self.clock.tick(self.fps)

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
        self.game_display.fill(self.snake.color, rect=[self.snake.segments[0].pos_x, self.snake.segments[0].pos_y, snake.block_size, snake.block_size])
        for s in self.snake.segments[1:]:
            self.game_display.fill(self.snake.color2, rect=[s.pos_x, s.pos_y, snake.block_size, snake.block_size])

    def draw_fruit(self, fruit):
        self.game_display.fill(self.red, rect=[fruit.pos_x, fruit.pos_y, fruit.block_size, fruit.block_size])

    def exit_game(self):
        pygame.quit()
        quit()
