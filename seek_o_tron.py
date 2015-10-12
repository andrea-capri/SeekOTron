import pyglet

from game import game_state


class SeekOTron:
    BOARD_WIDTH = 3
    BOARD_HEIGHT = 3

    def __init__(self):
        self.game_state = game_state.GameState(self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.window = pyglet.window.Window(resizable=True)
        self.key_input_enabled = False
        self.loot_image = pyglet.image.load('img/loot.png')
        self.robot_image = pyglet.image.load('img/robot.png')
        self.win_banner_image = pyglet.image.load('img/win_text.png')

        @self.window.event
        def on_draw():
            self.window.clear()
            self.draw_grid()
            self.draw_loot()
            self.draw_robot()
            if self.game_state.is_won():
                self.draw_win_banner()

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.handle_keys(symbol)

    def handle_keys(self, symbol):
        if self.game_state.is_won():
            self.game_state = game_state.GameState(self.BOARD_WIDTH, self.BOARD_HEIGHT)
        elif symbol == pyglet.window.key.Q:
            exit()
        elif symbol == pyglet.window.key.K:
            self.key_input_enabled = not self.key_input_enabled
            if self.key_input_enabled:
                print("Hey, I'm now listening for keyboard input")
            else:
                print("Hey, I'm no longer listening for keyboard input")
        elif symbol == pyglet.window.key.D:
            print("Debug output follows...")
            print("Player location: " + str(self.game_state.player_position))
            print("Loot location: " + str(self.game_state.loot_position))
        elif self.key_input_enabled:
            if symbol == pyglet.window.key.RIGHT:
                self.game_state.move_right()
            elif symbol == pyglet.window.key.LEFT:
                self.game_state.move_left()
            elif symbol == pyglet.window.key.UP:
                self.game_state.move_up()
            elif symbol == pyglet.window.key.DOWN:
                self.game_state.move_down()

    def draw_grid(self):
        # Draw horizontal lines
        for row in range(1, self.game_state.height):
            y = (self.window.get_size()[1] // self.game_state.height) * row
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                 ('v2i', (0, y, self.window.get_size()[0], y)),
                                 ('c3B', (255, 255, 255, 255, 255, 255))
                                 )

        # Draw vertical lines
        for col in range(1, self.game_state.width):
            x = (self.window.get_size()[0] // self.game_state.width) * col
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                                 ('v2i', (x, 0, x, self.window.get_size()[1])),
                                 ('c3B', (255, 255, 255, 255, 255, 255))
                                 )

    def get_square_size(self):
        return (self.window.get_size()[0] // self.game_state.width,
                self.window.get_size()[1] // self.game_state.height)

    def get_square_aspect_ratio(self):
        tile_size = self.get_square_size()
        return tile_size[0] / tile_size[1]

    def draw_robot(self):
        sprite = pyglet.sprite.Sprite(self.robot_image)
        # Scale sprite
        robot_aspect_ratio = self.robot_image.width / self.robot_image.height
        square_size = self.get_square_size()
        square_aspect = self.get_square_aspect_ratio()
        if square_aspect > robot_aspect_ratio:  # tiles are relatively wider, scale based on tile height
            scaling_coeff = square_size[1] / sprite.height
        else:  # tiles are relatively taller, scale based on tile width
            scaling_coeff = square_size[0] / sprite.width
        sprite.scale = scaling_coeff - 0.01  # scale just a little smaller so image always fits
        # Position sprite
        robot_square_x, robot_square_y = self.game_state.player_position
        sprite_horizontal_buffer = (square_size[0] - sprite.width) // 2
        sprite.x = robot_square_x * square_size[0] + sprite_horizontal_buffer
        sprite_vertical_buffer = (square_size[1] - sprite.height) // 2
        sprite.y = robot_square_y * square_size[1] + sprite_vertical_buffer
        # Draw it
        sprite.draw()

    def draw_loot(self):
        sprite = pyglet.sprite.Sprite(self.loot_image)
        # Scale sprite
        loot_aspect_ratio = self.loot_image.width / self.loot_image.height
        square_size = self.get_square_size()
        square_aspect = self.get_square_aspect_ratio()
        if square_aspect > loot_aspect_ratio:  # tiles are relatively wider, scale based on tile height
            scaling_coeff = square_size[1] / sprite.height
        else:  # tiles are relatively taller, scale based on tile width
            scaling_coeff = square_size[0] / sprite.width
        sprite.scale = scaling_coeff - 0.01  # scale just a little smaller so image always fits
        # Position sprite
        loot_square_x, loot_square_y = self.game_state.loot_position
        sprite_horizontal_buffer = (square_size[0] - sprite.width) // 2
        sprite.x = loot_square_x * square_size[0] + sprite_horizontal_buffer
        sprite_vertical_buffer = (square_size[1] - sprite.height) // 2
        sprite.y = loot_square_y * square_size[1] + sprite_vertical_buffer
        # Draw it
        sprite.draw()

    def draw_win_banner(self):
        sprite = pyglet.sprite.Sprite(self.win_banner_image)
        # Scale sprite
        banner_aspect_ratio = self.win_banner_image.width / self.win_banner_image.height
        window_aspect = self.window.get_size()[0] / self.window.get_size()[1]
        if window_aspect > banner_aspect_ratio:  # window is relatively wider, scale based on window height
            scaling_coeff = self.window.get_size()[1] / sprite.height
        else:  # window is relatively taller, scale based on window width
            scaling_coeff = self.window.get_size()[0] / sprite.width
        sprite.scale = scaling_coeff - 0.01  # scale just a little smaller so image always fits
        # Position sprite
        sprite_horizontal_buffer = (self.window.get_size()[0] - sprite.width) // 2
        sprite.x = sprite_horizontal_buffer
        sprite_vertical_buffer = (self.window.get_size()[1] - sprite.height) // 2
        sprite.y = sprite_vertical_buffer
        # Draw it
        sprite.draw()

    def game_loop(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = SeekOTron()
    game.game_loop()
