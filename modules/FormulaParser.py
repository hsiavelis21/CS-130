"""
Formula Parser
================
This parser considers types of literal values, cell references, arithimetic
expressions involving cell references. 

if not a number an error results. 
Cell references are of the form [col][row]. Also, cells in a different sheet are
refernecs as shee_name![col][row]. Note, cell references are case insesitive. 
If an error, the cell value set to the error. Error types for formula parsing are:
    1. PARSE_ERROR --> a formule cannot be parsed; string representation is #ERROR!
    2. CIRCULAR_REFERENCE --> a cell's formula references itself, either directly, 
    or indirectly through one or more chains of other cells; string representation 
    is #CIRCREF!
    3. BAD_REFERENCE --> a cell reference in a formula is invalif for some reason - 
    either the sheet name (if specified) is unknown, or the cell reference exceeds 
    the maximum location; string representation is #REF!
    4.  BAD_NAME --> a function name in a formula is unrecognized; string representation
    is #NAME?
"""
from operator import add, sub, mul, truediv as div, neg, pos, concat
import Spreadsheet
import Cell
import CellContents
import sheets
import decimal
from lark import *
from lark.visitors import Interpreter, visit_children_decor


#This is the subclass of Interpreter used for Lark  
class EvaluateFormula(Interpreter):
    number = decimal

    def __init__(self, wrkbk= None):
        self.vars = {}
        self.workbook = wrkbk

    def number(self, tree):
        return decimal.Decimal(tree.children[0])
        
    def string(self, tree):
        return tree.children[0][1:-1]

    @visit_children_decor
    def error(self, tree):
        return tree[0]

    @visit_children_decor
    def cell(self, tree):
        curr_cell = tree[1]
        curr_spreadsheet = tree[0]
        curr_workbook = self.workbook

        try:    
            cell_value = curr_workbook.get_cell_value(curr_spreadsheet, curr_cell)
        except KeyError: 
            return "#REF!" #Sheet not in workbook 
        
        for i in range(curr_workbook.num_sheets()):
            curr_sheet = curr_workbook.spreadsheet_list[i]
       
        if curr_cell not in curr_sheet.dict.keys():
            return "#REF!" #Not valid location

        return cell_value
    
    @visit_children_decor   
    def parens(self, tree):
        return tree[0]

    @visit_children_decor   
    def add_expr(self, tree):
        oper = tree[1]

        if tree[0] == "#REF!" or tree[2] == "#REF!":
            return "#REF!"

        try:
            if oper == '+':
                return add(tree[0], tree[2])
            return sub(tree[0], tree[2])
        except TypeError:
            return "#VALUE!"
      
    @visit_children_decor   
    def mul_expr(self, tree):
        oper = tree[1]
        
        if tree[0] == "#REF!" or tree[2] == "#REF!":
            return "#REF!"

        try:
            if oper == '*':
                return mul(tree[0], tree[2])
            if tree[2] == 0:
                return "#DIV/0!"
            return div(tree[0], tree[2])
        except TypeError:
            return "#VALUE!"
    
    @visit_children_decor   
    def unary_op(self, tree):
        size = len(tree)
        oper = tree[0]

        if tree[1] == "#REF!":
            return "#REF!"
        try:
            if oper == "-":
                return neg(tree[1])
            return pos(tree[1])
        except TypeError:
            return "#VALUE!"
    
    @visit_children_decor
    def concat_expr(self, tree):
        
        if len(tree) == 2:
            if tree[0] == "#REF!" or tree[1] == "#REF!":
                return "#REF!"

        return concat(tree[0], tree[1])

########### CREATE PARSER THAT SEPERATES SHEETNAME FROM LOCATION 
class ParseFormula():

    formula_parser = Lark.open('formulas.lark', start='formula')
    formula = formula_parser.parse

    def __init__(self, input_formula='', wrkbk=None):
        self.formula =input_formula
        self.workbook = wrkbk
        try: 
            self.tree = self.formula_parser.parse(self.formula)
        except (UnexpectedEOF,UnexpectedCharacters):
            self.formula = "=#ERROR!"
            self.tree = self.formula_parser.parse(self.formula)
 
   #Creates the stack that is used to check for strongly connected components
    def DFS_iter(self, source):
        seen = set()
        #source is a cell location which is a string
        stack = [source]

        result = []

        while (len(stack) != 0):
            curr_cell_location = stack.pop()
            curr_cell_index, curr_cell_name = self.seperate_spdsheet_name(curr_cell_location)
            curr_cell =  sheets.get_cell(curr_cell_index, curr_cell_name) 
            curr_refs = curr_cell.get_references() 

            if curr_cell_location not in seen:
                result.append(curr_cell_location)
                seen.add(curr_cell_location)
                for a, b in curr_refs:
                    stack.append(b)
        return result


    #reverses the stack so the cells can be iterated through backwards
    #LOCATION STILL HAS SHEET NAME ATTACHED
    def reverse_stack(self, stack):
        adj_lst = [] #consists of cells represented by location

        for cell_location in reversed(stack):
            curr_cell_index, curr_cell_name = self.seperate_spdsheet_name(cell_location)
            curr_cell =  sheets.get_cell(curr_cell_index, curr_cell_name) 
            for a,b in curr_cell.get_references():
                adj_lst.append((b,a))
        return adj_lst

    #Goes through DFS in the reverse list and returns a list of cycles
    def reverse_DFS_iter(stack, adj_lst):
        seen = set()

        cycles = []
        curr_cycle = []

        while (len(stack) != 0):
            curr_cell_location = stack.pop()
            if curr_cell_location not in seen:
                seen.add(curr_cell_location)
                
                curr_cycle.append(curr_cell_location) #starting with this cycle
                for b,a in adj_lst:
                    if b == curr_cell_location: #found an edge 
                        if a in curr_cycle:
                            cycles.append(curr_cycle)
                            curr_cycle = []
                        stack.append(a)
        return cycles


    #seen is a dictionary with keys as cells with values of whether seen or not
    #stack is a list of cells

    #updates spreadsheet and evaluates cells 
    #CALL THIS FUNCTION TO EVALUATE FORMUALS OUTSIDE OF FORMULA PARSER
    def evaluate_spreadsheet(self, source):
        #assume references are lists as SHEETNAME![COL][ROW]
        
        #Priorty 2, check for circular refs
        stack = self.DFS_iter(source)
        adj_list = self.reverse_stack(stack)
        cycles = self.reverse_DFS_iter(stack, adj_list)

        #cycles contains a list of cycles, where each cycle contains the locations of cells in the circular ref
        for cycle in cycles:
            for cell in cycle:
                cell_index, cell_name = self.seperate_spdsheet_name(cell)
                cell_contents = sheets.Workbook.get_cell_contents(cell_index, cell_name) 
                cell_contents.contents = "=#CIRCREF!"
        
        #Priorty #1: Parse, parse errors might happen
        index, name = self.seperate_spdsheet_name(source)
        cell_contents = sheets.Workbook.get_cell_contents(index, name) 
        tree = self.formula_parser.parse(cell_contents)

        self.update_spreadsheet(self, source)

        return self.evaluate_tree(tree)


    def evaluate_tree(self, tr):
        return EvaluateFormula(self.workbook).visit(tr)

    def update_spreadsheet(self, source):
        #Performs a Topological sort on the workbook and evaluates each source

        update_order = self.iter_topological_sort(source)
        for cell_location in update_order:
            cell_index, cell_name = self.seperate_spdsheet_name(cell_location)
            cell_contents = sheets.Workbook.get_cell_contents(cell_index, cell_name) 
            tree = self.formula_parser.parse(cell_contents)

            #do not update cell_contents, stays the same
            #update cell_type
            #update cell_value

            new_value = self.evaluate_tree(self, tree)
            curr_cell = sheets.Workbook.get_cell_from_spreadsheet(cell_index, cell_name) 
            val, cont, typ = CellContents.edit_value_for_type(new_value, curr_cell.type, cell_contents)

            cell_contents.value = val
            #aslo update type?
            cell_contents.type = CellContents.find_type(val)
    
    def iter_topological_sort(self, source):
        seen = set()
        stack = [source]

        while(len(stack) != 0):
            curr = stack.pop()
            if curr not in seen:
                self.topological_sort_helper(seen, stack, source)
        
        return stack[::-1]
    

    def ref_generator(self, cell):
        index, name = self.seperate_spdsheet_name(cell)
        curr_cell = sheets.Workbook.get_cell_contents(index, name) #PARSE LOCATION
        for ref in curr_cell.get_references:
            yield ref

    def topological_sort_helper(self, seen, stack, source):
        curr_stack = [(source,self.ref_generator(source))]

        while (len(curr_stack) != 0):

            source, generated = curr_stack[-1]
            seen.add(source)

            curr_stack.pop()

            indicator = True
            while indicator:
                generated_next = next(generated, None)
                if generated_next is None:
                    indicator = False
                    stack.append(source)
                    continue

                if generated_next not in seen:
                    curr_stack.append((source, generated))
                    curr_stack.appen((generated_next, self.ref_generator(generated_next)))
                    indicator = False


    def seperate_spdsheet_name(self, location):
        slice_index = location.index('!')
        return location[0:slice_index], location[(slice_index + 1):]

if __name__ == "__main__":
    workbook_2 = sheets.Workbook()
    index, sheet_name = workbook_2.new_sheet("SHEET2")
    workbook_2.set_cell_contents("SHEET2", "A1", "=SHEET2!B1")
    workbook_2.set_cell_contents("SHEET2", "B1", "=SHEET2!C1")
    workbook_2.set_cell_contents("SHEET2", "C1", "= 1/0")


    parse_tree = ParseFormula("=SHEET2!B1", workbook_2)
    print(parse_tree.evaluate_tree())
    




 
    #do concat with non strings
    #empty cells with arithmetic and empty cells with concatenation
    #if error in cell, make sure cell has right error


   
 


