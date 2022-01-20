import context
import sheets
import pytest

def test():
    # Should print the version number of your sheets library,
    # which should be 1.0 for the first project.
    print(f'Using sheets engine version {sheets.version}')

    # Make a new empty workbook
    wb = sheets.Workbook()

    assert(wb.num_sheets() == 0)
    assert(wb.list_sheets() == [])
    (index, name) = wb.new_sheet()

    assert(wb.list_sheets() == ['Sheet1'])

    # Should print:  New spreadsheet "Sheet1" at index 0
    print(f'New spreadsheet "{name}" at index {index}')
    
    (index, name) = wb.new_sheet('@test')

    with pytest.raises(ValueError):
        (index, name) = wb.new_sheet('')
        (index, name) = wb.new_sheet(' hi')
        (index, name) = wb.new_sheet('hi ')
        (index, name) = wb.new_sheet(' hi ')
        (index, name) = wb.new_sheet('  ')

        (index, name) = wb.new_sheet('test"test')
        (index, name) = wb.new_sheet("t'est")
        (index, name) = wb.new_sheet('t~est')

        (index, name) = wb.new_sheet('@TeST')
        (index, name) = wb.new_sheet('sHeEt1')

    (index, name) = wb.new_sheet('Sheet2')
    (index, name) = wb.new_sheet()
    assert(name == 'Sheet3')
    (index, name) = wb.new_sheet()
    assert(name == 'Sheet4')

    assert(wb.num_sheets() == 5)

    wb.del_sheet('Sheet4')
    assert(wb.num_sheets() == 4)

    wb.del_sheet('@tESt')
    assert(wb.num_sheets() == 3)

    wb.del_sheet('Sheet2')
    assert(wb.num_sheets() == 2)

    (index, name) = wb.new_sheet()
    assert(name == 'Sheet2')

    (index, name) = wb.new_sheet('Sheet4')
    (index, name) = wb.new_sheet()

    assert(name == 'Sheet5')

    with pytest.raises(KeyError):
        wb.del_sheet('test')

   
    wb.del_sheet('Sheet4')
    wb.del_sheet('Sheet5')


    assert(wb.list_sheets() == ['Sheet1', 'Sheet3', 'Sheet2'])

    assert(wb.get_sheet_extent('Sheet1') == (0,0))
    wb.set_cell_contents('Sheet1', 'A1', "'test")
    assert(wb.get_sheet_extent('Sheet1') == (1,1))
    wb.set_cell_contents('Sheet1', 'A5', '130')
    assert(wb.get_sheet_extent('Sheet1') == (1, 5))

    assert(wb.get_cell_contents('Sheet1', 'A1') == "'test")
    assert(wb.get_cell_value('Sheet1', 'A1') == "test")
    assert(wb.get_cell_contents('Sheet1', 'A5') == '130')
    assert(wb.get_cell_value('Sheet1', 'A5' == 130))






