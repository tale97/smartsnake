__author__ = 'tales.cpadua'


class SnakeSegment():
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def to_tuple(self):
        return (self.pos_x, self.pos_y)


class Snake():
    def __init__(self, display, block_size, pos_x=80, pos_y=80):
        self.color2 = (0,0,0)
        self.color = (0, 155, 0)
        self.display = display
        self.block_size = block_size
        self.x_velocity = 0
        self.y_velocity = (-1)*self.block_size
        self.segments = []
        self.segments.append(SnakeSegment(pos_x, pos_y))
        self.prev_x_vel = 0
        self.prev_y_vel = 0

    def segments_list(self):
        seg_list = []
        for seg in self.segments:
            seg_tuple = seg.to_tuple()
            seg_list.append(seg_tuple)
        return seg_list

    # To turn, we keep velocity variables for x and y direction, and then we sum it to the position
    # The snake will be always moving, so the event handler will only change the movement direction
    # The snake cannot go directly to the opposite direction. The first if of these methods assure this
    def turn_left(self):
        if self.x_velocity > 0:
            return
        self.x_velocity = (-1)*self.block_size
        self.y_velocity = 0

    def turn_right(self):
        if self.x_velocity < 0:
            return
        self.x_velocity = self.block_size
        self.y_velocity = 0

    def turn_down(self):
        if self.y_velocity < 0:
            return
        self.y_velocity = self.block_size
        self.x_velocity = 0

    def turn_up(self):
        if self.y_velocity > 0:
            return
        self.y_velocity = (-1)*self.block_size
        self.x_velocity = 0

    def add_segment(self):
        segment = SnakeSegment(self.segments[-1].pos_x, self.segments[-1].pos_y)
        segment.color = (155,155,155)
        self.segments.append(segment)

    # Here we sum the velocity to the position. Note that negative values will decrease the position value, since
    # sum negative number is the same as subtracting a positive one
    #
    def move(self):
        next_x_pos = self.segments[0].pos_x + self.x_velocity
        next_y_pos = self.segments[0].pos_y + self.y_velocity
        self.segments.pop()
        self.segments.insert(0, SnakeSegment(next_x_pos, next_y_pos))

    def move_virtual(self,head_pos, seg_list, x_vel, y_vel):
        pos_x, pos_y = head_pos
        next_x_pos = pos_x + x_vel
        next_y_pos = pos_y + y_vel
        seg_list.pop()
        seg_list.insert(0, SnakeSegment(next_x_pos, next_y_pos))
        new_head_pos = (next_x_pos, next_y_pos)
        return (new_head_pos, seg_list, x_vel, y_vel)

    #reset snake to initial values
    def reset_snake(self):
        self.segments = []
        self.segments.append(SnakeSegment(300, 300))
        self.x_velocity = 0
        self.y_velocity = (-1)*self.block_size
