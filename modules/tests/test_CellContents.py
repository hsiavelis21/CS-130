import modules.CellContents

def test_filter_contents():
    test_string1 = ''
    test_string2 = ' '
    test_string3 = '        '
    test_string4 = ' test'
    test_string5 = 'test '
    test_string6 = 'test'
    test_string7 = ' test '
    test_string8 = 'test1 test2'
    test_string9 = ' test1 test2'
    test_string10 = ' test1 test2 '
    test_string11 = 'test1 test2 '

    assert('' == CellContents.filter_contents(test_string1))
    assert('' == CellContents.filter_contents(test_string2))
    assert('' == CellContents.filter_contents(test_string3))
    assert('test' == CellContents.filter_contents(test_string4))
    assert('test' == CellContents.filter_contents(test_string5))
    assert('test' == CellContents.filter_contents(test_string6))
    assert('test' == CellContents.filter_contents(test_string7))
    assert('test1 test2' == CellContents.filter_contents(test_string8))
    assert('test1 test2' == CellContents.filter_contents(test_string9))
    assert('test1 test2' == CellContents.filter_contents(test_string10))
    assert('test1 test2' == CellContents.filter_contents(test_string11))

    print('ALL FILTER CONTENTS TESTS PASS')