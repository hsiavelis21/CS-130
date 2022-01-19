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
from CellErrorType import CellErrorType
from CellError import CellError
from sheets import Workbook
import decimal
from lark import *
from lark.visitors import Interpreter, visit_children_decor


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
        cell_value = self.workbook.get_cell_value(curr_spreadsheet, curr_cell)

        return cell_value
    
    @visit_children_decor   
    def parens(self, tree):
        return tree[0]

    @visit_children_decor   
    def add_expr(self, tree):
        oper = tree[1]
        print(1)

        try:
            if oper == '+':
                print(1)
                return add(tree[0], tree[2])
            return sub(tree[0], tree[2])
        except TypeError:
            return "#VALUE!"
      
    @visit_children_decor   
    def mul_expr(self, tree):
        oper = tree[1]

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
        try:
            if oper == "-":
                return neg(tree[1])
            return pos(tree[1])
        except TypeError:
            return "#VALUE!"
    
    @visit_children_decor
    def concat_expr(self, tree):
        return concat(tree[0], tree[1])


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

            #CellErrorType.TYPE_ERROR
            #the formula parser sets the value, not the contents
            #according to the spec, the cell contents correspond to the string representation
            #of the error while the value is the corresponding
       

    #prints tree nicely
    def print_tree_pretty(self):
        print(self.tree.pretty())

    def evaluate_tree(self):
        return EvaluateFormula(self.workbook).visit(self.tree)


if __name__ == '__main__':

    parse_tree = ParseFormula("= + 1 ")
    print(parse_tree.evaluate_tree()) #returing none for cell refs



# DO REF AND CIRC ERRORS


   
 


