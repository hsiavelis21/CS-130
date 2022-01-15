from Cell import *

cell1 = Cell(('A1'))
cell2 = Cell(('A15')) 
cell3 = Cell(('B12')) 
cell4 = Cell('AZ1') 
cell5 = Cell('CD10') 
cell6 = Cell('SH1001') 
cell7 = Cell('XYZ99')
cell8 = Cell('EFGH1234')
cell9 = Cell('ZZZZ9999') 

def test_find_location():
    assert(cell1.get_indices() == (1, 1))
    assert(cell2.get_indices() == (1, 15))
    assert(cell3.get_indices() == (2, 12))
    assert(cell4.get_indices() == (52, 1))
    assert(cell5.get_indices() == (2708, 10))
    assert(cell6.get_indices() == (502, 1001))
    assert(cell7.get_indices() == (16900, 99))
    assert(cell8.get_indices() == (92126, 1234))
    assert(cell9.get_indices() == (475254, 9999))

   