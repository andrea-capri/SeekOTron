import pyglet
import game_state


class SeekOTron:
    def __init__(self):
        self.game_state = game_state
        self.window = pyglet.window.Window(resizable=True)
        self.key_input_enabled = False

        @self.window.event
        def on_draw():
            self.window.clear()

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.handle_keys(symbol)

    def handle_keys(self, symbol):
        if symbol == pyglet.window.key.Q:
            exit()
        if symbol == pyglet.window.key.K:
            print("hey")
            self.key_input = not self.key_input

    def game_loop(self):
        pyglet.app.run()


if __name__ == "__main__":
    game = SeekOTron()
    game.game_loop()
