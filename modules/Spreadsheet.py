from Cell import Cell

class Spreadsheet:

    MAX_CELL = 'ZZZZ9999'
    MAX_ROW = 10 #9999
    MAX_COL = 10 #475254


    # Empty sheet constructor
    # Properties of a spreadsheet: matrix of cells
    def __init__(self, name = ""):
        self.name = name

        # Extent is formatted as ([col], [row])
        self.extent = (0, 0)

        self.dict = {}

    def get_name(self):
        return self.name

    def set_name(self, new_label):
        self.name = new_label

    def get_extent(self):
        return self.extent

    def set_extent(self, new_extent):
        self.extent = new_extent

    # Given a row and column index (input is 1-indexed), return the corresponding spreadsheet string location
    # Location must be 1 indexed.
    def convert_indices_to_location(self, r, c):
        # Convert 0-indexed indices to 1-index

        col = ""
        A = ord('A')
        while True:
            if c > 26:
                c, remainder = divmod(c - 1, 26)
                col += chr(remainder + A)
            else:
                col = chr(c + A - 1) + col
                break

        # Spreadsheet location format is [col][row]
        return col + str(r)
                

    # given location in string format [col][row], return separate column and row strings ex) A15, B12
    # WILL GIVE 1-INDEXED VALUES
    '''def convert_location_to_indices(self, location):
        row = ''
        col = ''
        for i in range(len(location)):
            if location[i].isnumeric(): # if character is a letter, it belongs to 
                row += location[i]
            else:
                col += location[i]

        col = self.cast_column_to_number(col)
        row = int(row)

        return(row, col)

    def cast_column_to_number(self, col):
    #col is a string of letters
        num = 0
        size = len(col) - 1
        for index in range(len(col)):
            num += (26 ** (index)) * (ord(col[size - index]) - 64)
        return num'''

    #edits an EXISTING STATEMENTS or adds a NEW cell
    def set_spreadsheet_cell_contents(self, location, new_contents):

        # Convert location to indices on spreadsheet
        row, col = Cell.convert_location_to_indices(location)

        # Check if location is a valid location on the spreadsheet
        if row < 1 or row > 9999 or col < 1 or col > 475254:
            raise ValueError('Cell location is invalid.')

        new_cell = Cell(location, new_contents)

        # Case 1: Cell at specified location has non-empty contents 
        if location in self.dict.keys():
            curr_cell = self.dict[location]

            # CASE 1.1: New cell has empty contents
            if new_cell.get_type() == 'EMPTY'
            # Change extent and remove the cell out of the dictionary
                del self.dict[location]
                self.extent = self.get_new_extent(location)

            else:
                curr_cell.set_cell_contents(new_contents) # Note, referencing is done in abstraction layers
                curr_cell.set_cell_value(new_contents)
       
        else:
        # CASE 2: Cell at specified location has empty contents
            if new_cell.get_type() != 'EMPTY':

                self.dict[location] = new_cell

                new_row, new_col = Cell.convert_location_to_indices(location)

                self.extent[0] = max(self.extent[0], new_col)
                self.extent[1] = max(self.extent[1], new_row)

    
    # If the cell at [row, col] does not exist, return the new extent of the spreadsheet. If row, col
    # is less than the current extent, return the current extent
    def get_new_extent(self, location):

        row, col = Cell.convert_location_to_indices(location)

        if row < self.extent[1] and col < self.extent[0]:
            return self.extent

        else:
            max_row = row
            max_col = col

            for cell in self.dict:
                curr_row, curr_col = Cell.convert_location_to_indices(cell)
                max_row = max(max_row, curr_row)
                max_col = max(max_col, curr_col)

        return max_row, max_col


    #gets an existing celll
    def get_spreadsheet_cell_contents(self, location):
        if not location not in self.dict.keys():
            raise ValueError("Not a valid cell location.")

        return self.dict[location].get_cell_contents()

    def get_spreadsheet_cell_value(self, location):

        if not location not in self.dict.keys():
            raise ValueError("Not a valid cell location.")

        return self.dict[location].get_cell_value()

        





