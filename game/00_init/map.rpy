init python:

    class Map():

        def __init__(self, game):
            self.game = game
            self.map_data = load_map("map.png")
            self.map_cell_width = len(self.map_data[0])
            self.map_cell_height = len(self.map_data)

            self.world_map = {}

            self.cell_size = 30
            self.cell_img = Solid("#000", xsize=self.cell_size, ysize=self.cell_size)
            
            self.half_map_width = (self.cell_size * self.map_cell_width) // 2
            self.half_map_height = (self.cell_size * self.map_cell_height) // 2

            self.get_map()


        def get_map(self):
            for y, row in enumerate(self.map_data):
                for x, value in enumerate(row):
                    if (value):
                        self.world_map[(x, y)] = value


        def pos_to_coord(self, pos_x, pos_y):

            return (int(pos_x / self.cell_size), int(pos_y / self.cell_size))

        #def draw_2d(self, render, width, height, st, at):
        def draw_2d(self, canvas):    

            for coord, value in self.world_map.items():
                
                x, y = coord

                canvas.rect("#444", (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size), 2)

