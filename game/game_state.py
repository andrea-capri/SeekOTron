import random


class GameState:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player_position = (random.randint(0, width - 1), random.randint(0, height - 1))
        self.loot_position = (random.randint(0, width - 1), random.randint(0, height - 1))
        # recalculate loot pos while it's the same as player pos
        while self.player_position == self.loot_position:
            self.loot_position = (random.randint(0, width - 1), random.randint(0, height - 1))

    def move_right(self):
        if self.player_position[0] < self.width - 1:
            self.player_position = (self.player_position[0] + 1, self.player_position[1])

    def move_left(self):
        if self.player_position[0] > 0:
            self.player_position = (self.player_position[0] - 1, self.player_position[1])

    def move_up(self):
        if self.player_position[1] < self.height - 1:
            self.player_position = (self.player_position[0], self.player_position[1] + 1)

    def move_down(self):
        if self.player_position[1] > 0:
            self.player_position = (self.player_position[0], self.player_position[1] - 1)

    def is_won(self):
        return self.player_position == self.loot_position
