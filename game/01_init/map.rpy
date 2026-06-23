init python:

    class Map():

        def __init__(self, game, path="images/fps/maps/map.png"):
            self.game = game
            map_data, self.player_start_pos = load_map(path)

            self.world_map = {}
            self.nav_map = []
            self.create_map(map_data)


        def create_map(self, map_data):
            self.nav_map = [[0 for _ in range(len(map_data[0]))] for _ in range(len(map_data))]
            for y, row in enumerate(map_data):
                for x, value in enumerate(row):
                    if (value > 0):
                        self.world_map[(x, y)] = value
                    
                    self.nav_map[y][x] = 0 if value < 1 else 1


        def draw_2d(self, canvas):    

            for pos, value in self.world_map.items():
                
                x, y = pos

                canvas.rect("#444", (x * self.game.scale, y * self.game.scale, self.game.scale, self.game.scale), 2)


        def is_wall(self, x, y):
            return (int(x), int(y)) in self.world_map
