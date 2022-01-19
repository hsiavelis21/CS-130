from decimal import *
import FormulaParser
import CellError
import CellErrorType

class CellContents:

    def __init__(self, contents='', wrkbk =''):
        self.contents = self.filter_contents(contents)
        self.workbook = wrkbk
        self.type = self.find_type(contents)
        self.value = ''
        self.set_value(self.type, contents, self.workbook)
        self.references = []

    def get_contents(self):
        return self.contents
        

    def set_contents(self, new_content, new_workbook):
        self.contents = self.filter_contents(new_content)
        self.workbook = new_workbook
        self.type = self.find_type(new_content)
        self.set_value(self.type, new_content, new_workbook)
        #incorporate references here 


    # remove white space, update contents
    def filter_contents(self, contents):
        new_contents = contents.strip()
        if new_contents == '':
            return None
        else:
            return new_contents

    #remove whitespaces
    #update cell contents to have no white space

    

    # input: filtered contents of cell (string input)
    # output: the type of the contents;
    # possible types: formula, string, literal value, empty cell (none type)
    def find_type(self, contents=''):
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
    def set_value(self, contents_type, contents, workbook):
        # self.value = ???

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
                self.set_contentS = CellErrorType.CellErrorType.CIRCULAR_REFERENCE
            elif self.value == "#REF!":
                self.set_contents = CellErrorType.CellErrorType.BAD_REFERENCE
            elif self.value == "#NAME?":
                self.set_contents = CellErrorType.CellErrorType.BAD_NAME
            elif self.value == "#VALUE!":
                self.set_contents = CellErrorType.CellErrorType.TYPE_ERROR
            elif self.value == "#DIV/0!":
                self.set_contentX = CellErrorType.CellErrorType.DIVIDE_BY_ZERO
            
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
        return self.value
        
    def is_empty(self):
        return self.contents == None

     #adds cells that the current cell references
    def add_reference(self, ref):
        self.references.append(ref)

    #gets cells that the current cell references
    def get_references(self):
        return self.references
    
    def remove_reference(self, index):
        self.references.pop(index)