import util
import random
import copy
import time
from gamelogic.autogame import Game as game
#import gamelogic.autogame as game

class Agent:
    def __init__(self, screen_width, screen_height, block_size):
        self.new_game = True
        self.solve_path = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.succesor_count = 0
        #self.game = Game(160, 160, 20)

    def get_path(self, state, food_pos):
        pass

    def at_food(self, state, food_pos):
        head_pos = state[0]
        return head_pos == food_pos

    def return_agent_name(self):
        return "Not defined"

    def is_collision(self, head_pos, snake_segment = list()):
        pos_x, pos_y = head_pos
        if pos_x < 0 or \
                pos_x > self.screen_width - self.block_size:
            return True
        if pos_y < 0 or \
                pos_y > self.screen_height - self.block_size:
            return True

        else:
            for (x,y) in snake_segment:
                if pos_x == x and pos_y == y:
                    return True
            return False

    def get_succesors(self, state):
        head_pos, segment_list, x_vel, y_vel = state
        successors = []
        for ((new_xvel, new_yvel), action) in [((-1*self.block_size,0),"left"), ((1*self.block_size,0),"right"), ((0,-1*self.block_size),"up"), ((0,1*self.block_size), "down")]:
            if (new_xvel*x_vel < 0) or (new_yvel*y_vel < 0):
                pass
            else:
                new_snake = self.move_virtual(head_pos, segment_list, new_xvel, new_yvel)
                if not self.is_collision(new_snake[0], new_snake[1][1:]):
                    successors.append((new_snake, action))
        return successors

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

    def food_found(self):
        print("BINGO")

    def longest_path(self, start, end):
        pass
#
# class IDF(Agent):
#     def DLS(self, state, action, food_pos, path, lim):
#         use_path = path
#         if self.at_food(state, food_pos):
#             return path.append(action)
#         elif lim <= 0:
#             use_path = []
#             return ["no sol"]
#
#         else:
#             # cut_off_occured = False
#             successors = self.get_succesors(state)
#             for cstate, action in successors:
#                 child_path = self.DLS(cstate, action, food_pos, lim -1)
#                 if child_path != ["no sol"]:
#                     use_path += (child_path)
#
#         return use_path
#

class BFSRand(Agent):

    def return_agent_name(self):
        return "BFSxRandom"

    def getpath(self, state, food_pos):
        original_head_pos = state
        fringe = util.Queue()
        expanded = []
        fringe.push((state, []))

        while not fringe.isEmpty():
            pop = fringe.pop()
            cur_state = pop[0]
            actions = pop[1]

            if cur_state in expanded:
                continue

            expanded.append(cur_state)

            if self.at_food(cur_state, food_pos):
                self.food_found()
                self.solve_path = actions
                break

            successors = self.get_succesors(cur_state)
            self.succesor_count += len(successors)
            """
            # if takes too long to find a path, take random safe action
            if self.succesor_count >= 25000:
                successors = self.get_succesors(original_head_pos)
                actions = []

                for state, action in successors:
                    actions.append(action)

                if actions:
                    self.solve_path = [random.choice(actions)]
                break
            """

            for state, action in successors:
                fringe.push((state, actions + [action]))
        self.new_game = False


class BFS(Agent):

    def return_agent_name(self):
        return "BFS"

    def getpath(self, state, food_pos):
        original_head_pos = state
        fringe = util.Queue()
        expanded = []
        fringe.push((state, []))

        while not fringe.isEmpty():
            pop = fringe.pop()
            cur_state = pop[0]
            actions = pop[1]

            if cur_state in expanded:
                continue

            expanded.append(cur_state)

            if self.at_food(cur_state, food_pos):
                self.food_found()
                self.solve_path = actions
                break

            successors = self.get_succesors(cur_state)
            self.succesor_count += len(successors)

            # if takes too long to find a path, take random safe action

            if self.succesor_count >= 25000:
                successors = self.get_succesors(original_head_pos)
                actions = []

                for state, action in successors:
                    actions.append(action)

                if actions:
                    self.solve_path = [random.choice(actions)]
                break

            for state, action in successors:
                fringe.push((state, actions + [action]))
        self.new_game = False



class SmartRandom(Agent):
    def return_agent_name(self):
        return "SmartRandom"

    def getpath(self, state, food_pos):
        successors = self.get_succesors(state)
        actions = []

        for state, action in successors:
            actions.append(action)
            print("possible actions:"),
            print(actions)
        if actions:
            self.solve_path = [random.choice(actions)]


class Random(Agent):
    def return_agent_name(self):
        return "Random"

    def getpath(self, state, food_pos):
        head, body, dx, dy = state
        actions = ["right", "left", "up", "down"]
        if dx < 0:
            actions.remove("right")
        elif dx > 0:
            actions.remove("left")
        elif dy < 0:
            actions.remove("down")
        elif dy > 0:
            actions.remove("up")
        self.solve_path = [random.choice(actions)]
        print("DEBUG"),
        print(self.solve_path)


class Greedy(Agent):
    def return_agent_name(self):
        return "Greedy"

    def getpath(self, state, food_pos):
        successors = self.get_succesors(state)
        actions = []
        m = 99999999
        best_action = ""
        for state, action in successors:
            temp = m
            m = min(m, util.manhattanDistance(state[0], food_pos))
            if not (m == temp):
                best_action = action
        self.solve_path = [best_action]



class Astar(Agent):
    def return_agent_name(self):
        return "Astar"

    def getpath(self, state, food_pos):
        original_head_pos = state
        fringe = util.PriorityQueueWithFunction(self.priority_function)
        expanded = []
        fringe.push((state, []))
        total_successors = 0
        ts2 = 0
        start = time.time()
        while not fringe.isEmpty():
            pop = fringe.pop()
            cur_state = pop[0]
            actions = pop[1]

            if cur_state in expanded:
                continue
            expanded.append(cur_state)

            if self.at_food(cur_state, food_pos):
                print("BINGO")
                self.solve_path = actions
                break

            successors = self.get_succesors(cur_state)
            total_successors += len(successors)
            ts2 += len(successors)

            if ts2 >= 25000:
                print(time.time() - start)
                print("expanded"),
                print(total_successors)
                ts2 = 0

            # if takes too long to find a path, take random safe action
            if total_successors >= 50000:
                successors = self.get_succesors(original_head_pos)
                actions = []

                for state, action in successors:
                    actions.append(action)
                print("safe actions:"),
                print(actions)
                if actions:
                    self.solve_path = [random.choice(actions)]
                break

            for state, action in successors:
                fringe.push((state, actions + [action]))
        print("TOTAL EXPANDED:"),
        print(total_successors)
        self.new_game = False

    def priority_function(self, state):
        #fruit = (self.fruit.pos_y, self.fruit.pos_x)
        item, action = state
        game.priofunc_astar(game, state)
        #return util.manhattanDistance(item[0], fruit)
