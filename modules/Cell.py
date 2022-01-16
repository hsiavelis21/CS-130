import CellContents

class Cell:
    
    # location is in format [col][row]; i.e. BR453
    def __init__(self, location, cell_contents=''):
        row, col = self.convert_location_to_indices(location).upper() # To access cell in matrix, subtract 1 from the row and column values
        self.row = row
        self.col = col
        self.cell_contents = cell_contents


    # given location in string format [col][row], return separate column and row strings ex) A15, B12
    # OUR MATRIX IS 0-INDEXED WHILE THE SPREADSHEET ITSELF IS ONE INDEXED; FIND LOCATION WILL GIVE 1-INDEXED VALUES
    def convert_location_to_indices(self, location):
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
        return num
        
    # DIFFERENT FROM FIND_INDICES; given cell object, return cell's row and col index
    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    # Return contents object of cell
    def get_cell_contents(self):
        return self.cell_contents.get_contents()

    def set_cell_contents(self, new_contents):
        self.set_contents(new_contents)

    # Return cell's value 
    def get_cell_value(self):
        return self.cell_contents.get_value()

    def set_cell_value(self, new_contents):
        self.set_value(new_contents)

    def set_cell_index(self, r, c):
        self.row = r
        self.col = c

    def get_cell_index(self):
        return (self.row, self.col)

    def is_empty(self):
        return self.cell_contents.is_empty()

    #gets cells that the current cell references
    def add_content_reference(self):
        return self.add_reference()

    #gets cells that the current cell references
    def get_content_references(self):
        return self.get_references()
    
    #removes a reference that the cell no longer references
    def remove_content_reference(self, ref):
        references = self.get_references()
        for i in range(len(references)):
            if references[i].get_index() == ref.get_index():
                #remove since it is the same cell
                self.remove_reference(i)
        
        



