import CellContents

class Cell:
    
    # location is in format [col][row]; i.e. BR453
    def __init__(self, location, cell_contents=''):
        row, col = self.find_location(location) # To access cell in matrix, subtract 1 from the row and column values
        self.row = row
        self.col = col
        self.cell_contents = cell_contents

    #check to make sure not greater than 9999 or less than 1 
    def check_valid_cell_locations(self, location):
        pass

    # given location in string format [col][row], return separate column and row strings ex) A15, B12
    # OUR MATRIX IS 0-INDEXED WHILE THE SPREADSHEET ITSELF IS ONE INDEXED; FIND LOCATION WILL GIVE 1-INDEXED VALUES
    def find_location(location): 
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
        
        



