init python:

    class Map():

        def __init__(self):
            self.map_data = load_map("map.png")
            self.map_cell_width = len(self.map_data[0])
            self.map_cell_height = len(self.map_data)
            
            self.world_map = {}

            self.cell_size = 25
            self.cell_img = Solid("#000", xsize=self.cell_size, ysize=self.cell_size)
            
            self.half_map_width = (self.cell_size * self.map_cell_width) // 2
            self.half_map_height = (self.cell_size * self.map_cell_height) // 2

            self.get_map()


        def get_map(self):
            for y, row in enumerate(self.map_data):
                for x, value in enumerate(row):
                    if (value):
                        self.world_map[(x, y)] = value


        #def draw_2d(self, render, width, height, st, at):
        def draw_2d(self, canvas, center_offset):    

            x_offset, y_offset = center_offset
            x_offset -= self.half_map_width
            y_offset -= self.half_map_height
            
            for coord, value in self.world_map.items():
                
                x, y = coord

                canvas.rect("#444", (x * self.cell_size + x_offset, y * self.cell_size + y_offset, self.cell_size, self.cell_size), 2)

