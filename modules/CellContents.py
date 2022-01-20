from decimal import *
from pdb import lasti2lineno
import FormulaParser
import CellError
import CellErrorType

class CellContents:

    def __init__(self, contents='', wrkbk ='', loc = "", sprdsheet =""):
        self.contents = self.filter_contents(contents)
        self.workbook = wrkbk
        self.type = self.find_type(contents)
        self.value = ''
        self.set_value(self.type, contents, self.workbook)
        self.references = [] #stored as SHEET![COL][ROW]
        self.location = loc
        self.spreadsheet = sprdsheet

    def get_contents(self):
        return self.contents
        

    def set_contents(self, new_content, new_workbook):
        self.contents = self.filter_contents(new_content)
        self.workbook = new_workbook
        self.type = self.find_type(new_content)
        self.set_value(self.type, new_content, new_workbook)
        #incorporate references here 

        #only cell references if a formula
        if self.type == 'FORMULA':
            operators = ['+', '-', '=', '/', '*', '&', '(', ')']
            lst = self.contents.split()
            operands = []

            #parses cell references out of formula
            curr_index = 0
            for index in range(len(lst)):
                if lst[index] in operators:
                    #want to find the value to the left and right 
                    for i in range(curr_index, index):
                        operand = lst[curr_index:index]
                        curr_index = index + 1
                        operands.append(operand)
            
            clean_operands = [item for item in operands if item != ""]
            
            #adds sheet name to the references that do not have them yet 
            for i in range(len(clean_operands)):
                if '!' not in clean_operands[i]:
                    update = self.spreadsheet + '!' + clean_operands[i]
                    clean_operands[i] = update 
            self.references = clean_operands 

                
        


            #can have the sheet name or not 
            #if no, append current sheet name
            #add to self.refs



        #need to parse and add cell refs 


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



    #Assume the cell contents have already been parsed and the cell value is the approriate value
    def edit_value_for_type(self, cell_value, cell_type, cell_contents):
        #ADD CURRENT SHEET NAME:
        #CHECK IF AN ERROR 
        if cell_value == "#ERROR!": #UPDATE TYPE TOO 
            cell_contents = CellErrorType.CellErrorType.PARSE_ERROR
        elif cell_value == "#CIRCREF!":
            cell_contents = CellErrorType.CellErrorType.CIRCULAR_REFERENCE
        elif cell_value == "#REF!":
            cell_contents = CellErrorType.CellErrorType.BAD_REFERENCE
        elif cell_value == "#NAME?":
            cell_contents = CellErrorType.CellErrorType.BAD_NAME
        elif cell_value == "#VALUE!":
            cell_contents = CellErrorType.CellErrorType.TYPE_ERROR
        elif cell_value == "#DIV/0!":
            cell_contents = CellErrorType.CellErrorType.DIVIDE_BY_ZERO
        elif cell_type == 'LITERAL':
        # REMOVE ALL TRAILING ZEROS FROM DECIMAL VALUE
            if '.' in cell_value:
                for i in range(len(cell_value)-1, -1, -1):
                    if cell_value[i] == '0':
                        new_value = cell_value[:i]
                    else:
                        if cell_value[i] == '.':
                            cell_value = cell_value[:i]
                        break
            cell_value = Decimal(cell_value)
        return cell_value, cell_contents, cell_type


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

            #ADD CURRENT SHEET NAME:
             
            cell_location = self.location
            cell_spreadsheet = self.spreadsheet
            new_location = str(cell_spreadsheet) + '!' + cell_location 
            #if spreadsheet name is not here, add it 
            curr_tree =  FormulaParser.ParseFormula(contents, workbook)
            self.value = curr_tree.evaluate_spreadsheet(new_location)

            new_value, new_contents, new_type = self.edit_value_for_type(self.value, contents_type, contents)
            self.value = new_value
            self.contents = new_contents
            self.type = new_type




    #Def check_for_sheet_names(self, contents, )
    
    def get_value(self): #parse for cell references
        return self.value
        
    def is_empty(self):
        return self.contents == None

     #adds cells that the current cell references
     #REFERENCES ARE TUPLES JUST LIKE EDGES
     #(a, b) a references b 
    def add_reference(self, ref):
        self.references.append(ref)

    #gets cells that the current cell references
    def get_references(self):
        return self.references
    
    def remove_reference(self, index): #instead of index, pop location
        self.references.pop(index)