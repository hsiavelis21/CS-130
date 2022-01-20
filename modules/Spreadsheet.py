import Cell

class Spreadsheet:

    # A spreadsheet containing zero or more defined cells.

    MAX_CELL = 'ZZZZ9999'
    MAX_ROW = 10 #9999
    MAX_COL = 10 #475254

    def __init__(self, name='', wrkbk=''):
        # Initialize a new empty spreadsheet with its name and workbook
        # it belongs to
        self.name = name
        self.workbook = wrkbk

        # Extent is formatted as ([col], [row])
        self.extent = (0, 0)

        self.dict = {}
    
    def get_name(self):
        # Return the name of the spreadsheet
        return self.name

    def set_name(self, new_label):
        # Set the name of the spreadsheet to new_label
        self.name = new_label

    def get_extent(self):
        # Return a tuple denoting the extent of the spreadsheet as ([col], [row])
        return self.extent

    def set_extent(self, new_extent):
        # Set the extent of the spreadsheet to new_extent
        self.extent = new_extent

    def get_cell(self, location):
        return self.dict[location]

    # Given a row and column index (input is 1-indexed), return the corresponding spreadsheet string location
    # Location must be 1 indexed.
    def convert_indices_to_location(self, r, c):
        # Given a row and column index (input is 1-indexed), return the 
        # corresponding spreadsheet string location. Location must be 1 indexed.
        
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
                

    def convert_location_to_indices(self, location):
        # given location in string format [col][row], return separate column and 
        # row strings ex) A15, B12

        row = ''
        col = ''
        for i in range(len(location)):
            if location[i].isnumeric():
                row += location[i]
            else:
                col += location[i]

        col = self.cast_column_to_number(col)
        row = int(row)

        return(row, col)

    def cast_column_to_number(self, col):
    # Given a string denoting a column, return a numeric value for the column
        num = 0
        size = len(col) - 1
        for index in range(len(col)):
            num += (26 ** (index)) * (ord(col[size - index]) - 64)
        return num

   
    def set_spreadsheet_cell_contents(self, location, new_contents, new_workbook):
        # Updates the contents of an already existing cell in the spreadsheet or adds
        # contents to a new cell in the spreadsheet

        new_contents = new_contents.strip()
        # Convert location to indices on spreadsheet
        row, col = self.convert_location_to_indices(location)

        # Check if location is a valid location on the spreadsheet
        if row < 1 or row > 9999 or col < 1 or col > 475254:
            raise ValueError('Cell location is invalid.')

        new_cell = Cell.Cell(location, new_contents, new_workbook, self.name)

        # Case 1: Cell at specified location has non-empty contents 
        if location in self.dict.keys():
            curr_cell = self.dict[location]

            # CASE 1.1: New cell has empty contents
            if new_cell.get_cell_type() == 'EMPTY':
            # Change extent and remove the cell out of the dictionary
                del self.dict[location]
                self.extent = self.get_new_extent(location)

            else:
                curr_cell.set_cell_contents(new_contents, new_workbook) # Note, referencing is done in abstraction layers
                curr_cell.set_cell_value(new_contents, new_workbook)
       
        else:
        # CASE 2: Cell at specified location has empty contents
            if new_cell.get_cell_type() != 'EMPTY':

                self.dict[location] = new_cell

                new_row, new_col = self.convert_location_to_indices(location)
                
                self.extent = (max(self.extent[0], new_col), max(self.extent[1], new_row))


    def get_new_extent(self, location):
        # If the cell at the given location does not exist, return the new extent of the 
        # spreadsheet. If row, col is less than the current extent, return the current extent
        
        row, col = self.convert_location_to_indices(location)

        if row < self.extent[1] and col < self.extent[0]:
            return self.extent

        else:
            max_row = 0
            max_col = 0

            for cell in self.dict:
                curr_row, curr_col = self.convert_location_to_indices(cell)
                max_row = max(max_row, curr_row)
                max_col = max(max_col, curr_col)

        return max_row, max_col


    def get_spreadsheet_cell_contents(self, location):
        # Return the cell contents of an existing cell

        row, col = self.convert_location_to_indices(location)
        # Check if location is a valid location on the spreadsheet
        if row < 1 or row > 9999 or col < 1 or col > 475254:
            raise ValueError('Cell location is invalid.')
        
        # If location of cell on spreadsheet is empty:
        if not location in self.dict.keys():
            return None

        return self.dict[location].get_cell_contents()

    def get_spreadsheet_cell_value(self, location):
        # Return the cell value of an existing cell

        row, col = self.convert_location_to_indices(location)

        if row < 1 or row > 9999 or col < 1 or col > 475254:
            raise ValueError('Cell location is invalid.')
        
        if not location in self.dict.keys():
            return None

        return self.dict[location].get_cell_value()





