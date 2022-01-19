import decimal
import sheets
import pytest

def test():
    # Should print the version number of your sheets library,
    # which should be 1.0 for the first project.
    print(f'Using sheets engine version {sheets.version}')

    # Make a new empty workbook
    wb = sheets.Workbook()
    (index, name) = wb.new_sheet()

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

    (index, name) = wb.new_sheet('sheet4')
    (index, name) = wb.new_sheet()
    assert(name == 'Sheet5')




