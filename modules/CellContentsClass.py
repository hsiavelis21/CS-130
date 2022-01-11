class CellContents:

    def __init__(self, contents=''):

        self.contents = contents
        self.type = find_type(contents)
        self.value = set_value(self.type, contents)

    def get_contents(self):
        return self.contents

    def set_contents(self, new_content):
        self.contents = new_content
        self.type = find_type(new_content)

    # remove white space, update contents
    def filter_contents(self, contents):
        pass

    # input: contents of cell (string input)
    # output: the type of the contents;
    # possible types: formula, string, literal value, empty cell (none type)
    # look at CellContentsTypeClass.py
    def find_type(contents):
        pass

    def set_type(self, new_type):
        self.type = new_type

    def get_type(self):
        return self.type

    # given a content's type, convert the contents into a value that has Decimal type if content is a number,
    # Formula type if forumula, or keep as String if string (single quote), or None if type is None
    def set_value(self, type, contents):
        # self.value = ???
        pass

    def get_value(self):
        return self.value