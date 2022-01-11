import Cell

class Spreadsheet:

    MAX_CELL = 'ZZZ9999'

    # Empty sheet constructor
    # Properties of a spreadsheet: matrix of cells
    def __init__(self):
        # instead of starting it with empty matrix, maybe initialize it to be ZZZ x 9999 matrix with all empty cells
        self.matrix = [[]] 
        self.extent = (0, 0)

    def get_extent(self):
        return self.extent

    def set_extent(self, new_extent):
        self.extent = new_extent

    # location is a tuple
    # check if cell is empty or not
    # if empty, create new cell and add properties
    # if not empty, set cell properties to new properties and check if other cells reference
    def set_spreadsheet_cell_contents(self, location, new_contents):
        row, col = location
        curr_cell = self.matrix[row][col]





