from Spreadsheet import *

s1 = Spreadsheet('Test1')

def test_spreadsheet():

    assert(s1.get_name() == 'Test1')

    s1.set_name('TEST1')
    assert(s1.get_name() == 'TEST1')

    assert(s1.get_extent() == (0,0))

    s1.set_extent((5, 6))
    assert(s1.get_extent() == (5,6))

    assert(s1.convert_indices_to_location(0, 0) == 'A1')
    assert(s1.convert_indices_to_location(5, 26) == 'AA6')
    assert(s1.convert_indices_to_location(9998, 475253) == 'ZZZZ9999')