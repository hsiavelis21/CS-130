from typing import *
import Spreadsheet
import FormulaParser

#==============================================================================
# Caltech CS130 - Winter 2022
#
# This file specifies the API that we expect your implementation to conform to.
# You will likely want to move these classes into various files, but the tests
# will expect these to be available when the "sheets" module is imported.

# If you are unfamiliar with Python 3 type annotations, see the Python standard
# library documentation for the typing module here:
#
#     https://docs.python.org/3/library/typing.html

version = '1.0.0'

class Workbook:

    # A workbook containing zero or more named spreadsheets.
    #
    # Any and all operations on a workbook that may affect calculated cell
    # values should cause the workbook's contents to be updated properly.

    def __init__(self):
        # Initialize a new empty workbook.
        self.spreadsheet_list = []

    def num_sheets(self) -> int:
        # Return the number of spreadsheets in the workbook.
        return len(self.spreadsheet_list)
        

    def list_sheets(self) -> List[str]:
        # Return a list of the spreadsheet names in the workbook, with the
        # capitalization specified at creation, and in the order that the sheets
        # appear within the workbook.
        #
        # In this project, the sheet names appear in the order that the user
        # created them; later, when the user is able to move and copy sheets,
        # the ordering of the sheets in this function's result will also reflect
        # such operations.
        #
        # A user should be able to mutate the return-value without affecting the
        # workbook's internal state.
        lst = []
        for sheet in self.spreadsheet_list:
            lst.append(sheet.name)
        return lst

    def generate_spreadsheet_name(self):
        # Return a string that is a valid spreadsheet name. The string should not
        # contain any leading or trailing whitespaces and must not be the name of
        # an already existing spreadsheet.

        curr_number = self.num_sheets() + 1
        new_name = "Sheet" + str(curr_number)

        curr_spreadsheet_names = set()
        for s in self.spreadsheet_list:
            curr_spreadsheet_names.add(s.get_name().lower())

        while new_name.lower() in curr_spreadsheet_names:
            curr_number += 1
            new_name = "Sheet" + str(curr_number)

        return new_name


    def new_sheet(self, sheet_name: Optional[str] = None) -> Tuple[int, str]:
        # Add a new sheet to the workbook.  If the sheet name is specified, it
        # must be unique.  If the sheet name is None, a unique sheet name is
        # generated.  "Uniqueness" is determined in a case-insensitive manner,
        # but the case specified for the sheet name is preserved.
        #
        # The function returns a tuple with two elements:
        # (0-based index of sheet in workbook, sheet name).  This allows the
        # function to report the sheet's name when it is auto-generated.
        #
        # If the spreadsheet name is an empty string (not None), or it is
        # otherwise invalid, a ValueError is raised.

        new_name = sheet_name

        valid_chars = set(['.', '?', ':', ';', '!', '@', '#', '$', '%',
        '^', '&', '*', '(', ')', '-', '_'])

        #if name is None, generate name
        if sheet_name == None:
            new_name = self.generate_spreadsheet_name()
        else:
        # Checks if sheet_name is empty string or if it has leading or trailing white spaces
            if sheet_name.strip() != sheet_name or sheet_name == '':
                raise ValueError('Invalid sheet name.')

            # Checks if sheet_name already exists in workbook (case insensitive)
            curr_spreadsheet_names = set()
            for s in self.spreadsheet_list:
                curr_spreadsheet_names.add(s.get_name().lower())

            if sheet_name.lower() in curr_spreadsheet_names:
                raise ValueError('Invalid sheet name.')

            if '"' in sheet_name or "'" in sheet_name:
                raise ValueError('Invalid sheet name.')

            for letter in sheet_name:
                if not letter.isalnum() and letter not in valid_chars:
                    raise ValueError('Invalid sheet name.') 

        curr_sheet = Spreadsheet.Spreadsheet(new_name)
        self.spreadsheet_list.append(curr_sheet)
        return (len(self.spreadsheet_list) - 1, new_name)

    def del_sheet(self, sheet_name: str) -> None:
        # Delete the spreadsheet with the specified name.
        #
        # The sheet name match is case-insensitive; the text must match but the
        # case does not have to.
        #
        # If the specified sheet name is not found, a KeyError is raised.

        for i in range(self.num_sheets()):
            curr_sheet = self.spreadsheet_list[i]
            if curr_sheet.name.lower() == sheet_name.lower():
                self.spreadsheet_list.pop(i)
        raise KeyError("Specified sheet name is not found.")

    def get_sheet_extent(self, sheet_name: str) -> Tuple[int, int]:
        # Return a tuple (num-cols, num-rows) indicating the current extent of
        # the specified spreadsheet.
        #
        # The sheet name match is case-insensitive; the text must match but the
        # case does not have to.
        #
        # If the specified sheet name is not found, a KeyError is raised.

        for i in range(self.num_sheets()):
            curr_sheet = self.spreadsheet_list[i]
            if curr_sheet.name.lower() == sheet_name.lower():
                return curr_sheet.get_extent()
        raise KeyError("Specified sheet name is not found.") 

    def set_cell_contents(self, sheet_name: str, location: str,
                          contents: Optional[str]) -> None:
        # Set the contents of the specified cell on the specified sheet.
        #
        # The sheet name match is case-insensitive; the text must match but the
        # case does not have to.  Additionally, the cell location can be
        # specified in any case.
        #
        # If the specified sheet name is not found, a KeyError is raised.
        # If the cell location is invalid, a ValueError is raised.
        #
        # A cell may be set to "empty" by specifying a contents of None.
        #
        # Leading and trailing whitespace are removed from the contents before
        # storing them in the cell.  Storing a zero-length string "" (or a
        # string composed entirely of whitespace) is equivalent to setting the
        # cell contents to None.
        #
        # If the cell contents appear to be a formula, and the formula is
        # invalid for some reason, this method does not raise an exception;
        # rather, the cell's value will be a CellError object indicating the
        # naure of the issue.

        #iterate through sheets
        for i in range(self.num_sheets()):
            curr_sheet = self.spreadsheet_list[i]
            if curr_sheet.name.lower() == sheet_name.lower():
                #get the cell and change contents
                curr_sheet.set_spreadsheet_cell_contents(location, contents, self)
                return
        
        raise KeyError("Specified sheet name is not found.")


        

    def get_cell_contents(self, sheet_name: str, location: str) -> Optional[str]:
        # Return the contents of the specified cell on the specified sheet.
        #
        # The sheet name match is case-insensitive; the text must match but the
        # case does not have to.  Additionally, the cell location can be
        # specified in any case.
        #
        # If the specified sheet name is not found, a KeyError is raised.
        #
        # Any string returned by this function will not have leading or trailing
        # whitespace, as this whitespace will have been stripped off by the
        # set_cell_contents() function.
        #
        # This method will never return a zero-length string; instead, empty
        # cells are indicated by a value of None.
        for i in range(self.num_sheets()):
            curr_sheet = self.spreadsheet_list[i]
            if curr_sheet.name.lower() == sheet_name.lower():
                #get the cell and change contents
                curr_sheet.get_spreadsheet_cell_contents(location)
                return
        
        raise KeyError("Specified sheet name is not found.")

    def get_cell_value(self, sheet_name: str, location: str) -> Any:
        # Return the evaluated value of the specified cell on the specified
        # sheet.
        #
        # The sheet name match is case-insensitive; the text must match but the
        # case does not have to.  Additionally, the cell location can be
        # specified in any case.
        #
        # If the specified sheet name is not found, a KeyError is raised.
        # If the cell location is invalid, a ValueError is raised.
        #
        # The value of empty cells is None.  Non-empty cells may contain a
        # value of str, decimal.Decimal, or CellError.
        #
        # Decimal values will not have trailing zeros to the right of any
        # decimal place, and will not include a decimal place if the value is a
        # whole number.  For example, this function would not return
        # Decimal('1.000'); rather it would return Decimal('1').
        for i in range(self.num_sheets()):
            curr_sheet = self.spreadsheet_list[i]
            if curr_sheet.name.lower() == sheet_name.lower():
                #get the cell and change contents
                #curr_sheet.get_spreadsheet_cell_value(location)
                return curr_sheet.get_spreadsheet_cell_value(location)
        
        raise KeyError("Specified sheet name is not found.")


    def get_cell_from_spreadsheet(self, sheet_name, location):
        #parse for sheet name and [col][rol]
        for i in range(self.num_sheets()):
            curr_sheet = self.spreadsheet_list[i]
            if curr_sheet.name.lower() == sheet_name.lower():
                #get the cell and change contents
                return curr_sheet.get_cell(location)




