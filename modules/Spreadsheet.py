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

        new_cell = Cell(row, col, new_contents)
        curr_row_extent = self.extent[0]
        curr_col_extent = self.extent[1]

        # If a new non-empty value is being put into an empty cell
        if curr_cell.is_empty() and not new_cell.is_empty():
             # if empty, create new cell and add properties; update extent if necessary
            self.set_extent(max(curr_row_extent, row), max(curr_col_extent, col))

        elif not curr_cell.is_empty() and new_cell.is_empty():
            new_row_extent, new_col_extent = self.get_new_extent(row, col)
            self.set_extent(new_row_extent, new_col_extent)

        # if not empty, set cell properties to new properties and check if other cells reference 
        #referencing is done in abstraction layers
        curr_cell.set_cell_contents(new_contents)
        curr_cell.set_cell_value(new_contents)
            #other cells referencing this cell

    # If the cell at [row, col] no longer exists, return the new extent of the spreadsheet. If row, col
    # is less than the current extent, return the current extent
    def get_new_extent(self, row, col):
        curr_row_extent, curr_col_extent = self.extent
        max_row_extent = max(row, curr_row_extent)
        max_col_extent = max(col, curr_col_extent)

        final_row_extent = 0
        final_col_extent = 0

        if row < curr_row_extent and col < curr_col_extent:
            return self.extent
        else:
            if row >= curr_row_extent:
                if curr_row_extent <= 1:
                    final_row_extent = 0

                for c in range(max_col_extent - 1, -1, -1):
                    for r in range(max_row_extent - 1, -1, -1):
                        if not self.matrix[r][c].is_empty():
                            final_row_extent = max(final_row_extent, r)
            
            if col >= curr_col_extent:
                if curr_row_extent <= 1:
                    final_col_extent = 0

                for r in range(max_row_extent-1, -1, -1):
                    for c in range(max_col_extent-1, -1, -1):
                        if not self.matrix[r][c].is_empty():
                            final_col_extent = max(final_col_extent, c)

        return final_row_extent, final_col_extent

        # row, col represents a cell that doees not change the extent
        if max_row_extent == curr_row_extent and max_col_extent == curr_col_extent:
            return (max_row_extent, max_col_extent)


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

        





