from django.db import models
from django.conf import settings
from random import randint

class Map(models.Model):
    name = models.CharField(max_length=128)
    data = models.CharField(max_length=10000)
    width = models.IntegerField()
    height = models.IntegerField()
    num_bombs = models.IntegerField()

    def mark(self, x, y):
        contents = self._get_contents(x, y)

        if contents == 'B':
            return -1
        elif contents == 'E':
            num_bombs = self._count_adj_bombs(x, y)
            self._change_contents(x, y, str(num_bombs))
            return num_bombs

    def _get_adj_empties(self, x, y):

        empties = [[x, y]]
        coords = self._build_adj_coords(x, y)

        for pair in coords:
            bombs = self._count_adj_bombs(pair[0], pair[1])
            empties.append(pair)

        return empties


    def _build_adj_coords(self, x, y):
        coords = [
          (x-1, y),
          (x-1, y-1),
          (x, y-1),
          (x+1, y-1),
          (x+1, y),
          (x+1, y+1),
          (x, y+1),
          (x-1, y+1)
        ]
        return coords

    def _count_adj_bombs(self, x, y):
        count = 0
        coords = self._build_adj_coords(x, y)

        stack = []

        # If this space is a bomb, just say so
        if self._get_contents(x, y) == 'B':
            return -1

        for pair in coords:
            out_of_bounds_x = pair[0] < 0 or pair[0] >= self.width
            out_of_bounds_y = pair[1] < 0 or pair[1] >= self.height

            if out_of_bounds_x or out_of_bounds_y:
                continue

            if self._get_contents(pair[0], pair[1]) == 'B':
                count += 1

        return count

    def _get_data_index(self, x, y):
        z = self.width * y
        index = z + x
        return index

    def _get_contents(self, x, y):
        index = self._get_data_index(x, y)
        c = self.data[index]
        return c

    def _change_contents(self, x, y, new_content):
        index = self._get_data_index(x, y)
        data = list(self.data)
        data[index] = new_content
        self.data = "".join(data)

    def generate_map(self):
        data = []

        # Make empty map
        for i in range(self.width * self.height):
            data.append('E')
        self.data = "".join(data)

        # Place the bombs
        for i in range(self.num_bombs):
            self._place_random_bomb()

    def _place_random_bomb(self):
        is_set = False

        while not is_set:
            randx = randint(0, self.width - 1)
            randy = randint(0, self.height - 1)

            if self._get_contents(randx, randy) == 'E':
                self._change_contents(randx, randy, 'B')
                is_set = True

    def get_map_matrix(self):

        matrix = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                content = self._get_contents(j, i)
                if content == 'B' or content == 'E':
                    content = ''
                row.append(content)
            matrix.append(row)

        return matrix







