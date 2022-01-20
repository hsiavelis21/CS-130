from decimal import *
import FormulaParser
import CellError
import CellErrorType

class CellContents:

    # The contents of a cell. The contents have one of the following types:
    # EMPTY, STRING, FORMULA, ERROR, STRING, LITERAL
    # Based on the contents' type, its value is found.

    def __init__(self, contents='', wrkbk =''):
        # Initialize the contents of a cell. 
        self.contents = self.filter_contents(contents)
        self.workbook = wrkbk
        self.type = self.find_type(contents)
        self.value = ''
        self.set_value(self.type, contents, self.workbook)
        self.references = []

    def get_contents(self):
        # Return the contents of the cell_contents object
        return self.contents
        

    def set_contents(self, new_content, new_workbook):
        # Set the contents of the current cell_contents object to new_content

        self.contents = self.filter_contents(new_content)
        self.workbook = new_workbook
        self.type = self.find_type(new_content)
        self.set_value(self.type, new_content, new_workbook)
        #incorporate references here 


    def filter_contents(self, contents):
        # Remove any leading/trailing whitespaces of the input
        new_contents = contents.strip()
        if new_contents == '':
            return None
        else:
            return new_contents


    def find_type(self, contents=''):
        
        # Given a string with no leading/trailing whitespaces, return the type
        # of the contents. possible types: formula, string, literal value, 
        # empty cell (none type)

        if contents == '':
            return 'EMPTY'

        if contents[0] == "'":
            return 'STRING'

        if contents[0] == '=':
            return 'FORMULA'
        
        if contents[0] == '#':
            return 'ERROR'

        else:
            dot_count = 0

            for char in contents:
                if char == '.':
                    dot_count += 1

                if dot_count > 1 or (char != '.' and not char.isnumeric()):
                    return 'STRING'
            
            return 'LITERAL'

    #Todo: NEEDS T0 BE CHANGED TO ADDRESS INVALID TYPE CHANGES
    def set_type(self, new_type):
        # Set the type of the cell_contents to new_type
        self.type = new_type #if None, means empty cell

    def get_type(self):
        # Get the type of the cell_contents object
        return self.type


    def set_value(self, contents_type, contents, workbook):
        # given a content's type, convert the contents into a value that
        # has Decimal type if content is a number, Formula type if formula, 
        # or keep as String if string (single quote), or None if type is None
        #
        # If the cell contents appear to be a formula, and the formula is
        # invalid for some reason, this method does not raise an exception;
        # rather, the cell's value will be a CellError object indicating the
        # nature of the issue.

        if contents_type == 'EMPTY':
            self.value = None

        if contents_type == 'STRING': #Get rid of quotation
            if contents[0] == "'":
                self.value = contents[1:]
            else:
                self.value = contents

        if contents_type == 'FORMULA':
            curr_tree =  FormulaParser.ParseFormula(contents, workbook)
            self.value = curr_tree.evaluate_tree()

            #CHECK IF AN ERROR 
            if self.value == "#ERROR!":
                self.contents = CellErrorType.CellErrorType.PARSE_ERROR
            elif self.value == "#CIRCREF!":
                self.contentS = CellErrorType.CellErrorType.CIRCULAR_REFERENCE
            elif self.value == "#REF!":
                self.contents = CellErrorType.CellErrorType.BAD_REFERENCE
            elif self.value == "#NAME?":
                self.contents = CellErrorType.CellErrorType.BAD_NAME
            elif self.value == "#VALUE!":
                self.contents = CellErrorType.CellErrorType.TYPE_ERROR
            elif self.value == "#DIV/0!":
                self.contents = CellErrorType.CellErrorType.DIVIDE_BY_ZERO
            
        if contents_type == 'LITERAL':
            # REMOVE ALL TRAILING ZEROS FROM CONTENTS
            if '.' in contents:
                for i in range(len(contents)-1, -1, -1):
                    if contents[i] == '0':
                        contents = contents[:i]
                    else:
                        if contents[i] == '.':
                            contents = contents[:i]
                        break
            self.value = Decimal(contents)


    def get_value(self): #parse for cell references
        # Return the value of the cell_contents object
        return self.value
        
    def is_empty(self):
        # Return whether or not the cell_contents object is empty
        return self.contents == None

    def add_reference(self, ref):
        # Adds cells that the current cell references

        self.references.append(ref)

    def get_references(self):
        # Return a list of cells that the current cell references
        return self.references
    
    def remove_reference(self, index):
        # Remove a reference that the current cell_contents object references
        # at given index.
        self.references.pop(index)