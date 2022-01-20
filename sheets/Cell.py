import CellContents

class Cell:
    
    # A cell containing its contents and its location on the spreadsheet

    # location is in format [col][row]; i.e. BR453
    def __init__(self, location, cell_contents='', wrkbk = ''):
        # Initialize a new cell in the spreadsheet at a specified location with
        # the given cell_contents in the workbook
        row, col = self.convert_location_to_indices(location.upper()) # row, col are 1 indexed
        self.row = row
        self.col = col
        self.workbook = wrkbk
        self.cell_contents = CellContents.CellContents(cell_contents, wrkbk)


    def convert_location_to_indices(self, location):
        # given location in string format [col][row], return separate column and row strings ex) A15, B12

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
        # Given a string denoting a column, return a numeric value for the column
    
        num = 0
        size = len(col) - 1
        for index in range(len(col)):
            num += (26 ** (index)) * (ord(col[size - index]) - 64)
        return num
        
    def get_row(self):
        # Return the cell's numerical row index
        return self.row

    def get_col(self):
        # Return the cell's numerical col index
        return self.col

    def get_cell_contents(self):
        # Return contents object of the cell
        return self.cell_contents.get_contents()

    def set_cell_contents(self, new_contents, new_workbook):
        # Set the contents of the cell to new_contents
        self.cell_contents.set_contents(new_contents, new_workbook)

    def get_cell_value(self):
        # Return cell's value 
        return self.cell_contents.get_value()

    def set_cell_value(self, new_contents, new_workbook):
        # Set the cell's value to the value of new_contents
        self.cell_contents.set_value(self.find_cell_type(new_contents), new_contents, new_workbook)

    def get_cell_type(self):
        # Get the type of the cell
        return self.cell_contents.get_type()

    def set_cell_type(self, new_type):
        # Set the type of the cell to new_type
        self.set_type(new_type)

    def find_cell_type(self, contents):
        # Find the type of the contents of the cell
        return self.cell_contents.find_type(contents)

    def set_cell_index(self, r, c):
        # Set the indices of the cell to r, c
        self.row = r
        self.col = c

    def get_cell_index(self):
        # Return the indices of the cell
        return (self.row, self.col)

    def is_empty(self):
        # Return True if the cell has no contents in it, False otherwise
        return self.cell_contents.is_empty()

    def add_content_reference(self):
        # Add a cell reference to the cells that the current cell references
        return self.add_reference()

    def get_content_references(self):
        # Return the list of cells that the current cell references
        return self.get_references()
    
    def remove_content_reference(self, ref):
        # Removes a reference that the cell no longer references

        references = self.get_references()
        for i in range(len(references)):
            if references[i].get_index() == ref.get_index():
                #remove since it is the same cell
                self.remove_reference(i)



