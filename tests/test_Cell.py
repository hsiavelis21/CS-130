import context
import sheets
import pytest

cell1 = Cell(('A1'))
cell2 = Cell(('A15')) 
cell3 = Cell(('B12')) 
cell4 = Cell('AZ1') 
cell5 = Cell('CD10') 
cell6 = Cell('SH1001') 
cell7 = Cell('XYZ99')
cell8 = Cell('EFGH1234')
cell9 = Cell('ZZZZ9999') 
cell10 = Cell('A2', '      ')

def test_find_location():
    assert(cell1.get_row() == 1)
    assert(cell1.get_col() == 1)
    assert(cell2.get_row() == 15)
    assert(cell2.get_col() == 1)
    assert(cell3.get_row() == 12)
    assert(cell3.get_col() == 2)
    assert(cell4.get_row() == 1)
    assert(cell4.get_col() == 52)
    assert(cell5.get_row() == 10)
    assert(cell5.get_col() == 82)
    assert(cell6.get_row() == 1001)
    assert(cell6.get_col() == 502)
    assert(cell7.get_row() == 99)
    assert(cell7.get_col() == 16900)
    assert(cell8.get_row() == 1234)
    assert(cell8.get_col() == 92126)
    assert(cell9.get_row() == 9999)
    assert(cell9.get_col() == 475254)

    assert(cell9.get_cell_type() == 'EMPTY')
    assert(cell9.get_cell_contents() == None)
    assert(cell10.get_cell_contents() == None)
   