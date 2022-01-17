from CellContents import *

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
test12 = CellContents('1.0')

def test_filter_contents():

    assert(None == test1.filter_contents('   '))
    assert('test' == test1.filter_contents('test'))
    assert('test' == test1.filter_contents(' test'))
    assert('test' == test1.filter_contents('  test   '))

def test_get_contents():
    assert(None == test1.get_contents())
    assert(None == test2.get_contents())
    assert(None == test3.get_contents())
    assert('test' == test4.get_contents())
    assert('test' == test5.get_contents())
    assert('test' == test6.get_contents())
    assert('test' == test7.get_contents())
    assert('test1 test2' == test8.get_contents())
    assert('test1 test2' == test9.get_contents())
    assert('test1 test2' == test10.get_contents())
    assert('test1 test2' == test11.get_contents())
    
def test_constructor():
    test1 = CellContents("'abc")
    test2 = CellContents('')

    assert(test1.find_type("'abc") == 'STRING')
    assert(test2.find_type() == 'EMPTY')

    test2.set_contents("'test")

    assert(test2.get_type()=="STRING")
