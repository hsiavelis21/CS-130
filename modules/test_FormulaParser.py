from ast import parse
from FormulaParser import *
import decimal 

#testing arithmetic formulas 
tree1 =  ParseFormula(('=1 + 2'))
tree2 =  ParseFormula(('=1 * 2')) 
tree3 =  ParseFormula(('=2/1')) 
tree4 =  ParseFormula('=1-2') 
tree5 =  ParseFormula('=2-1') 
tree6 =  ParseFormula('=1 - -2') 
tree7 =  ParseFormula('=1 - +2')
tree8 =  ParseFormula('=(1 + 2) * 3')
tree9 =  ParseFormula('=1 - 2 * 2') 

def test_evaluating_arithmetic():
    assert(tree1.evaluate_tree() == decimal.Decimal('3'))
    assert(tree2.evaluate_tree() == decimal.Decimal('2'))
    assert(tree3.evaluate_tree() == decimal.Decimal('2'))
    assert(tree4.evaluate_tree() == decimal.Decimal('-1'))
    assert(tree5.evaluate_tree() == decimal.Decimal('1'))
    assert(tree6.evaluate_tree() == decimal.Decimal('3'))
    assert(tree7.evaluate_tree() == decimal.Decimal('-1'))
    assert(tree8.evaluate_tree() == decimal.Decimal('9'))
    assert(tree9.evaluate_tree() == decimal.Decimal('-3'))

#testing string concatination
tree10 = ParseFormula("=\"   \"")
tree11 =  ParseFormula('=\"test\"')
tree12 =  ParseFormula('=\"test    \"') 
tree13 =  ParseFormula('=\"    test\"') 
tree14 =  ParseFormula('=\"    test    \"') 
tree15 =  ParseFormula('=\"test\" & \"again\"') 
tree16 =  ParseFormula('=\"test\" & \"     again\"') 
tree17 =  ParseFormula('=\"test     \" & \"    again\"') 
tree18 =  ParseFormula('=\"     test     \" & \"    again\"') 
tree19 =  ParseFormula('=\"     test\" & \"    again\"') 
tree20 =  ParseFormula('=\"test\" & \"again     \"') 
tree21 =  ParseFormula('=\"test     \" & \"again     \"') 
tree22 =  ParseFormula('=\"     test\" & \"again     \"') 
tree23 =  ParseFormula('=\"     test     \" & \"again     \"') 
tree24 =  ParseFormula('=\"test\" & \"     again     \"')
tree25 =  ParseFormula('=\"test     \" & \"     again     \"') 
tree26=  ParseFormula('=\"     test\" & \"     again     \"') 
tree27 =  ParseFormula('=\"     test    \" & \"     again     \"') 
tree28 =  ParseFormula('=\"test     \" & \"again\"') 
tree29 =  ParseFormula('=\"     test     \" & \"again\"') 
tree30 =  ParseFormula('=\"     test\" & \"again\"') 
tree31 = ParseFormula("=\"   \" & \"again\"")
tree32 = ParseFormula("=\"   \" & \"again     \"")
tree33 = ParseFormula("=\"   \" & \"     again\"")
tree34 = ParseFormula("=\"   \" & \"    again    \"")

def test_evaluating_concat():
    assert(tree10.evaluate_tree() == str("   "))
    assert(tree11.evaluate_tree() == str("test"))
    assert(tree12.evaluate_tree() == str("test    "))
    assert(tree13.evaluate_tree() == str("    test"))
    assert(tree14.evaluate_tree() == str("    test    "))
    assert(tree15.evaluate_tree() == str("testagain"))
    assert(tree16.evaluate_tree() == str("test     again"))
    assert(tree17.evaluate_tree() == str("test         again"))
    assert(tree18.evaluate_tree() == str("     test         again"))
    assert(tree19.evaluate_tree() == str("     test    again"))
    assert(tree20.evaluate_tree() == str("testagain     "))
    assert(tree21.evaluate_tree() == str("test     again     "))
    assert(tree22.evaluate_tree() == str("     testagain     "))
    assert(tree23.evaluate_tree() == str("     test     again     "))
    assert(tree24.evaluate_tree() == str("test     again     "))
    assert(tree25.evaluate_tree() == str("test          again     "))
    assert(tree26.evaluate_tree() == str("     test     again     "))
    assert(tree27.evaluate_tree() == str("     test         again     "))
    assert(tree28.evaluate_tree() == str("test     again"))
    assert(tree29.evaluate_tree() == str("     test     again"))
    assert(tree30.evaluate_tree() == str("     testagain"))
    assert(tree31.evaluate_tree() == str("   again"))
    assert(tree32.evaluate_tree() == str("   again     "))
    assert(tree33.evaluate_tree() == str("        again"))
    assert(tree34.evaluate_tree() == str("       again    "))


#ERROR!: cannot make sense of formula; i.e. missing operator, paraenthese...
#CIRCREF!:  refs itself (circular)
#REF!: cell location is out of bounds or sheet name is unknown 
#NAME?: function name in a formula is unrecognized, porbl --> NOT YET
#VALUE!: one or more parameters in the formula are of a different type or operation on unsupported type
#DIV/0 happens when a number is divided by 0

#testing cell errors without references
tree35 = ParseFormula("=1/0") #DIV/0!
tree36 = ParseFormula("= 1 + \"a\"") #VALUE!
tree37 = ParseFormula("= 1 - \"a\"") #VALUE!
tree38 = ParseFormula("= 1 * \"a\"") #VALUE!
tree40 = ParseFormula("= +\"a\"") #VALUE!
tree41 = ParseFormula("= -\"a\"") #VALUE!
tree42 = ParseFormula("= 1 + ") #ERROR!
tree43 = ParseFormula("= 1 * ") #ERROR!
tree44 = ParseFormula("= 1 - ") #ERROR!
tree45 = ParseFormula("= 1 / ") #ERROR!
tree46 = ParseFormula("= + ") #ERROR!
tree47 = ParseFormula("= -") #ERROR!
tree48 = ParseFormula("= * ") #ERROR!
tree49 = ParseFormula("= / ") #ERROR!
tree50 = ParseFormula("= + 1 ") 
tree51 = ParseFormula("= - 1 ") 
tree52 = ParseFormula("= * 1 ") #ERROR!
tree53 = ParseFormula("= / 1 ") #ERROR!
tree54 = ParseFormula("= 1 + + ") #ERROR!
tree55 = ParseFormula("= 1 ++ ") #ERROR!
tree56 = ParseFormula("= 1 + *") #ERROR!
tree57 = ParseFormula("= 1 + /") #ERROR!
tree58 = ParseFormula("= 1 + -") #ERROR!
tree59 = ParseFormula("= 1 +*") #ERROR!
tree60 = ParseFormula("= 1 +/") #ERROR!
tree61 = ParseFormula("= 1 +-") #ERROR!
tree62 = ParseFormula("= 1 #") #ERROR!
tree63 = ParseFormula("= 1 ^") #ERROR!

value_error = "#VALUE!"
error_error = "#ERROR!"
div_error = "#DIV/0!"

def test_cell_errors():
    assert(tree35.evaluate_tree() == div_error)
    assert(tree36.evaluate_tree() == value_error)
    assert(tree37.evaluate_tree() == value_error)
    assert(tree38.evaluate_tree() == value_error)
    assert(tree40.evaluate_tree() == value_error)
    assert(tree41.evaluate_tree() == value_error)
    assert(tree42.evaluate_tree() == error_error)
    assert(tree43.evaluate_tree() == error_error)
    assert(tree44.evaluate_tree() == error_error)
    assert(tree45.evaluate_tree() == error_error)
    assert(tree46.evaluate_tree() == error_error)
    assert(tree47.evaluate_tree() == error_error)
    assert(tree48.evaluate_tree() == error_error)
    assert(tree49.evaluate_tree() == error_error)
    assert(tree50.evaluate_tree() == decimal.Decimal("1"))
    assert(tree51.evaluate_tree() == decimal.Decimal("-1"))
    assert(tree52.evaluate_tree() == error_error)
    assert(tree53.evaluate_tree() == error_error)
    assert(tree54.evaluate_tree() == error_error)
    assert(tree55.evaluate_tree() == error_error)
    assert(tree56.evaluate_tree() == error_error)
    assert(tree57.evaluate_tree() == error_error)
    assert(tree58.evaluate_tree() == error_error)
    assert(tree59.evaluate_tree() == error_error)
    assert(tree60.evaluate_tree() == error_error)
    assert(tree61.evaluate_tree() == error_error)
    assert(tree62.evaluate_tree() == error_error)
    assert(tree63.evaluate_tree() == error_error)


#testing cell reference arithmetic
workbook_1 = Workbook()
index, sheet_name = workbook_1.new_sheet("SHEET1")
workbook_1.set_cell_contents("SHEET1", "A1", "1")
workbook_1.set_cell_contents("SHEET1", "A2", "2")

parse_tree = ParseFormula("= SHEET1!A1 + SHEET1!A2", workbook_1)
#testing cell reference errors















 



    