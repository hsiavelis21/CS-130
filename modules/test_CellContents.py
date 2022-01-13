from CellContents import *

def test_filter_contents():

    test1 = CellContents()
    test2 = CellContents('')
    test3 = CellContents(' ')
    test4 = CellContents('test')
    test5 = CellContents(' test')
    test6 = CellContents(' test ')
    test7 = CellContents('test ')
    test8 = CellContents('test1 test2')
    test9 = CellContents('test1 test2 ')
    test10 = CellContents(' test1 test2')
    test11 = CellContents(' test1 test2 ')

    assert('' == test1.filter_contents(' '))
    assert('' == test1.get_contents())


    print('ALL FILTER CONTENTS TESTS PASS')