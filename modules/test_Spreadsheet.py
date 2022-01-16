from Spreadsheet import *
import pytest

s1 = Spreadsheet('Test1')

def test_spreadsheet():

    assert(s1.get_name() == 'Test1')

    s1.set_name('TEST1')
    assert(s1.get_name() == 'TEST1')

    assert(s1.get_extent() == (0,0))

    s1.set_extent((5, 6))
    assert(s1.get_extent() == (5,6))

    assert(s1.convert_indices_to_location(1, 1) == 'A1')
    assert(s1.convert_indices_to_location(5, 26) == 'Z5')
    assert(s1.convert_indices_to_location(1001, 502) == 'SH1001')
    assert(s1.convert_indices_to_location(9999, 475254) == 'ZZZZ9999')


    # Check if ValueError is raised if invalid locations are put in

    invalid_index1 = s1.convert_indices_to_location(0, 0)
    invalid_index2 = s1.convert_indices_to_location(10000, 475255)
    
    with pytest.raises(ValueError):
        s1.set_spreadsheet_cell_contents(invalid_index1, "'hi")
        

    # CASE 2: Cell at specified location has empty contents
    s1.set_spreadsheet_cell_contents('A1', "'test")
    assert(s1.get_extent() == (1,1))


