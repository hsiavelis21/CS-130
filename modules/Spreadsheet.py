import Cell

class Spreadsheet:

    MAX_CELL = 'ZZZZ9999'
    MAX_ROW = 9999
    MAX_COL = 9999


    # Empty sheet constructor
    # Properties of a spreadsheet: matrix of cells
    def __init__(self, label = ""):
        # instead of starting it with empty matrix, maybe initialize it to be ZZZZ x 9999 matrix with all empty cells
        self.matrix = [[]]
        for r in range(self.MAX_ROW):
            for c in range(self.MAX_COL):
                self.matrix[r][c] = Cell(r,c)
        self.extent = (0, 0)
        self.name = label

    def get_name(self):
        return self.name

    def set_name(self, new_label):
        self.name = new_label

    def get_extent(self):
        return self.extent

    def set_extent(self, new_extent):
        self.extent = new_extent

    #edits an EXISTING STATEMENTS or adds a NEW cell
    def set_spreadsheet_cell_contents(self, location, new_contents):
        row, col = location
        curr_cell = self.matrix[row][col]

        if curr_cell.is_empty():
             # if empty, create new cell and add properties
            new_cell = Cell(row, col, new_contents)
            curr_row_extent = self.extent[0]
            curr_col_extent = self.extent[1]
            self.set_extent(max(curr_row_extent, row), max(curr_col_extent, col))
        else:
    # if not empty, set cell properties to new properties and check if other cells reference 
    #referencing is done in abstraction layers
            curr_cell.set_cell_contents(new_contents)
            curr_cell.set_cell_value(new_contents)
            #other cells referencing this cell
    
    #gets an existing celll
    def get_spreadsheet_cell_contents(self, location):
        row, col = location

        #make sure the location is valid
        if not self.matrix[row][col].check_valid_cell_locations(location):
            raise ValueError("Not a valid cell location.")
        return self.matrix[row][col].get_cell_contents()

    def get_spreadsheet_cell_value(self, location):

        row, col = location

        if not self.matrix[row][col].check_valid_cell_locations(location):
            raise ValueError("Not a valid cell location.")
        return self.matrix[row][col].get_cell_value()

        





