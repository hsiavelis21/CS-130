import enum

class CellContentsClass(enum.Enum):

    '''
    This enum specifies the types of content a cell can hold.
    '''

    FORMULA_CELL_TYPE = 1

    STRING_CELL_TYPE = 2
 
    # Decimal Value
    LITERAL_CELL_TYPE = 3

    NONE_CELL_TYPE = 4