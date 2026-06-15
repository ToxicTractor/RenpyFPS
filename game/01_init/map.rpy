init python:

    class Map():

        def __init__(self, game):
            self.game = game
            self.map_data = load_map("map.png")
            self.world_map = {}

            self.create_map()


        def create_map(self):
            for y, row in enumerate(self.map_data):
                for x, value in enumerate(row):
                    if (value):
                        self.world_map[(x, y)] = value


        def draw_2d(self, canvas):    

            for pos, value in self.world_map.items():
                
                x, y = pos

                canvas.rect("#444", (x * self.game.scale, y * self.game.scale, self.game.scale, self.game.scale), 2)

