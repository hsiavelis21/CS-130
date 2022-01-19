from Spreadsheet import *
import pytest

s1 = Spreadsheet('Test1')
s2 = Spreadsheet('Test2')

def test_spreadsheet_getters_and_setters():

    assert(s1.get_name() == 'Test1')

    s1.set_name('TEST1')
    assert(s1.get_name() == 'TEST1')

    assert(s1.get_extent() == (0,0))

    s1.set_extent((5, 6))
    assert(s1.get_extent() == (5,6))


def test_convert_indices_to_location():
    assert(s1.convert_indices_to_location(1, 1) == 'A1')
    assert(s1.convert_indices_to_location(5, 26) == 'Z5')
    assert(s1.convert_indices_to_location(1001, 502) == 'SH1001')
    assert(s1.convert_indices_to_location(9999, 475254) == 'ZZZZ9999')


def test_set_and_get_spreadsheet_cell_contents():
    # Check if ValueError is raised if invalid locations are put in
    invalid_index1 = s2.convert_indices_to_location(0, 0)
    invalid_index2 = s2.convert_indices_to_location(10000, 475255)
    
    with pytest.raises(ValueError):
        s2.set_spreadsheet_cell_contents(invalid_index1, "'hi")
        s2.set_spreadsheet_cell_contents(invalid_index2, "'hi")
        s2.set_spreadsheet_cell_contents('testing!!', "")
        s2.set_spreadsheet_cell_contents('', "")

    # CASE 2: Cell at specified location has empty contents
    s2.set_spreadsheet_cell_contents('A1', "'test")
    assert(s2.get_extent() == (1,1))
    
    assert(len(s2.dict) == 1)

    s2.set_spreadsheet_cell_contents('Z20', "1.234")
    assert(s2.get_extent() == (26, 20))

    # CASE 1: Cell at specified location has non-empty contents
    s2.set_spreadsheet_cell_contents('A1', "'new")
    assert(s2.get_spreadsheet_cell_contents('A1') == "'new")
    assert(s2.get_spreadsheet_cell_value('A1') == "new")
    assert(s2.dict['A1'].get_cell_type() == 'STRING')
    assert(s2.dict['Z20'].get_cell_type() == 'LITERAL')

    s2.set_spreadsheet_cell_contents('CDF500', '')
    assert(s2.get_extent() == (26, 20))
    assert(len(s2.dict) == 2)

    # CASE 1.1: New cell has empty contents
    s2.set_spreadsheet_cell_contents('B2', '1.3.')
    assert(s2.dict['B2'].get_cell_type() == 'STRING')
    s2.set_spreadsheet_cell_contents('B2', '')
    assert(len(s2.dict) == 2)
    assert(s2.get_spreadsheet_cell_contents('B3') is None)
    s2.set_spreadsheet_cell_contents('Z20', '    ')
    print(s2.dict.keys())
    assert(s2.get_extent() == (1,1))



