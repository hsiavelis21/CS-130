class CellContents:

    def __init__(self, contents=''):

        self.contents = self.filter_contents(contents)
        #self.type = self.find_type(contents)
        #self.value = self.set_value(self.type, contents)
        self.references = []

    def get_contents(self):
        return self.contents

    def set_contents(self, new_content):
        self.contents = self.filter_contents(new_content)
        self.type = self.find_type(new_content)
        self.value = self.set_value(self.type, new_content)
        #incorporate references here 


    # remove white space, update contents
    def filter_contents(self, contents):
        return contents.strip()

    #remove whitespaces
    #update cell contents to have no white space

    

    # input: contents of cell (string input)
    # output: the type of the contents;
    # possible types: formula, string, literal value, empty cell (none type)
    # look at CellContentsTypeClass.py
    def find_type(contents):
        pass

    def set_type(self, new_type):
        self.type = new_type #if None, means empty cell

    def get_type(self):
        return self.type

    # given a content's type, convert the contents into a value that has Decimal type if content is a number,
    # Formula type if forumula, or keep as String if string (single quote), or None if type is None
    #parse for cell references

    # If the cell contents appear to be a formula, and the formula is
        # invalid for some reason, this method does not raise an exception;
        # rather, the cell's value will be a CellError object indicating the
        # naure of the issue.
    def set_value(self, type, contents):
        # self.value = ???

        pass

    def get_value(self): #parse for cell references
        return self.value

    def is_empty(self):
        return self.contents == ''

     #adds cells that the current cell references
    def add_reference(self, ref):
        self.references.append(ref)

    #gets cells that the current cell references
    def get_references(self):
        return self.references
    
    def remove_reference(self, index):
        self.references.pop(index)