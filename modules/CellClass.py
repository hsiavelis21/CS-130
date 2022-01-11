import CellContentsClass

class Cell:
    
    # location is in format [col][row]; i.e. BR453
    def __init__(self, location, cell_contents=''):
        row, col = find_indices(location)
        self.row = row
        self.col = col
        self.cell_contents = cell_contents

    # given location in string format [col][row], return separate column and row strings
    def find_indices(location):
        pass

    # DIFFERENT FROM FIND_INDICES; given cell object, return cell's row and col index
    def get_indices(self):
        return self.row, self.col

    # Return contents object of cell
    def get_cell_contents(self):
        return self.cell_contents.get_contents()

    def set_cell_contents(self, new_contents):
        self.set_contents(new_contents)

    # Return cell's value
    def get_cell_value(self):
        return self.cell_contents.get_value()

    def set_cell_index(self, r, c):
        self.row = r
        self.col = c


