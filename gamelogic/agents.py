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
        self.states_expanded = 0
        self.end_game = False
        self.found_food = False
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

    def get_succesors2(self, state, depth):
        head_pos, segment_list, x_vel, y_vel, depth = state
        successors = []
        for ((new_xvel, new_yvel), action) in [((-1*self.block_size,0),"left"), ((1*self.block_size,0),"right"), ((0,-1*self.block_size),"up"), ((0,1*self.block_size), "down")]:
            if (new_xvel*x_vel < 0) or (new_yvel*y_vel < 0):
                pass
            else:
                depth += 1
                new_snake = self.move_virtual2(head_pos, segment_list, new_xvel, new_yvel, depth)
                if not self.is_collision(new_snake[0], new_snake[1][1:]):
                    successors.append((new_snake, action))
        return successors

    def move_virtual2(self, head, body, x_vel, y_vel, depth):
        """move virtual snake defined by head_pos and seg_list using x_vel and y_vel"""
        hx, hy = head
        next_x = hx + x_vel
        next_y = hy + y_vel
        new_head = (next_x, next_y)

        body_copy = copy.copy(body)
        body_copy.pop()
        body_copy.insert(0, (next_x, next_y))

        return (new_head, body_copy, x_vel, y_vel, depth)

    def food_found(self):
        self.found_food = True

    def longest_path(self, start, end):
        pass


###############################################################################
class BFS(Agent):
    def return_agent_name(self):
        return "BFS"

    def getpath(self, state, food_pos):
        self.found_food = False
        fringe = util.Queue()
        expanded = []
        fringe.push((state, []))
        expansion_counter = 0

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
            expansion_counter += len(successors)

            if expansion_counter >= 100000:
                print("Ended game because expanded too many states")
                self.solve_path = ""
                self.end_game = True
                break

            for state, action in successors:
                fringe.push((state, actions + [action]))
        self.new_game = False


class DFS(Agent):
    def return_agent_name(self):
        return "DFS"

    def getpath(self, state, food_pos):
        self.found_food = False
        #original_head_pos = state
        fringe = util.Stack()
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

            for state, action in successors:
                fringe.push((state, actions + [action]))
        self.new_game = False


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


class SmartRandom(Agent):
    def return_agent_name(self):
        return "SmartRandom"

    def getpath(self, state, food_pos):
        successors = self.get_succesors(state)
        actions = []

        for state, action in successors:
            actions.append(action)
        if actions:
            self.solve_path = [random.choice(actions)]


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


class BFSRand(Agent):
    def return_agent_name(self):
        return "BFSxRandom"

    def getpath(self, state, food_pos):
        self.found_food = False
        original_head_pos = state
        fringe = util.Queue()
        expanded = []
        fringe.push((state, []))
        expansion_counter = 0
        self.states_expanded = 0

        while not fringe.isEmpty():
            node = fringe.pop()
            cur_state = node[0]
            actions = node[1]

            if cur_state in expanded:
                continue
            expanded.append(cur_state)

            #check if found food
            if self.at_food(cur_state, food_pos):
                self.food_found()
                self.solve_path = actions
                break

            successors = self.get_succesors(cur_state)
            self.succesor_count += len(successors)
            expansion_counter += len(successors)
            self.states_expanded += len(successors)

            # if takes too long to find a path, take random safe action
            if expansion_counter >= 15000:
                print("Picking a Random save move...")
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


class BFS_DFS(Agent):
    def return_agent_name(self):
        return "BFS_DFS"

    def getpath(self, state, food_pos): #) = self.food_pos):
        self.found_food = False
        original_head_pos = state
        fringe = util.Queue()
        expanded = []
        fringe.push((state, []))
        total_successors = 0
        counter = 0

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
            total_successors += len(successors)
            counter += len(successors)

            if counter >= 15000:
                print("__DFS__")
                counter = 0
                print("expanded"),
                print(total_successors)

            # if takes too long to find a path, use DFS
            if total_successors >= 25000:
                print("Switching to DFS")
                fringe = util.Stack()
                expanded = []
                fringe.push((original_head_pos, []))

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
                    total_successors += len(successors)
                    counter += len(successors)

                    for state, action in successors:
                        fringe.push((state, actions + [action]))
                self.new_game = False
                break

            for state, action in successors:
                fringe.push((state, actions + [action]))
        self.new_game = False


class IDS(Agent):
    def return_agent_name(self):
        return "IDS"

    def getpath(self, state, food_pos, max_depth):
        self.found_food = False
        original_state = state
        fringe = util.Stack()
        expanded = []
        fringe.push((state, []))
        total_successors = 0
        found_food = False
        counter = 0

        # remove from stack
        while not fringe.isEmpty():
            pop = fringe.pop()
            cur_state = pop[0]
            actions = pop[1]

            if cur_state in expanded:
                continue
            expanded.append(cur_state)

            # if not goal state
            if self.at_food(cur_state, food_pos):
                self.food_found()
                self.solve_path = actions
                found_food = True
                break

            # if not at max depth
            if not (cur_state[4] >= max_depth):
                successors = self.get_succesors2(cur_state, cur_state[4])
                total_successors += len(successors)
                self.succesor_count += len(successors)
                counter += len(successors)

                if counter >= 100000:
                    print("TOO MANY STATES")
                    self.solve_path = ""
                    self.end_game = True
                    break

                for state, action in successors:
                    fringe.push((state, actions + [action]))

            if counter >= 100000:
                print("TOO MANY STATES")
                self.solve_path = ""
                self.end_game = True
                break

        if not self.found_food and not (max_depth >= 200):
            max_depth += 1
            self.getpath(original_state, food_pos, max_depth)

        self.new_game = False
