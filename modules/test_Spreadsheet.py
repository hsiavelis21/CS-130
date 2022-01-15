from Spreadsheet import *

s1 = Spreadsheet('Test1')

def test_spreadsheet():

    assert(s1.get_name() == 'Test1')

    s1.set_name('TEST1')
    assert(s1.get_name() == 'TEST1')
    
    assert(s1.get_extent() == (0,0))