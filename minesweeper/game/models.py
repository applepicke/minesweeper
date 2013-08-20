from django.db import models

class Map(models.Model):
    data = models.CharField(max_length=None)
    width = models.IntegerField()
    height = models.IntegerField()

    def mark(self, x, y):
        contents = self._get_contents(x, y)

        if contents == 'B':
            return 'dead'
        else if contents == 'E':
            return self._count_adj_bombs(x, y)

    def _count_adj_bombs(self, x, y):
        count = 0
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

        stack = []

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

