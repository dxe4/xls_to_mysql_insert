__author__ = 'foobar'
from xlrd import open_workbook
from xlrd.sheet import Sheet

class SheetReader(object):
    state_changes = {
        "schema": "table",
        "table": "cols",
        "cols":"rows",
        "rows": "table"
    }

    def __init__(self, sheet:Sheet):
        self.state = "schema"
        self.name = sheet.name
        self.state_callbacks = {
            "schema": self.process_schema,
            "table": self.process_table,
            "rows": self.process_rows,
            "cols": self.process_cols
        }
        self.current_table = None
        self.tables = []
        self.process_sheet(sheet)
        print(self.schema, "  ", self.table)

    def changes_state(f):
        def wrapper(*args):
            ret =  f(*args)
            args[0].state_process()
            return ret
        return wrapper

    def process_sheet(self, sheet:Sheet):
        print(" rows ", sheet.nrows, " cols ", sheet.ncols)
        for row_index in range(sheet.nrows):
            self.process_row(row_index, sheet)

    def process_row(self, row_index, sheet:Sheet):
        print(self.state)
        callback = self.state_callbacks[self.state]
        callback(row_index, sheet)

    def state_process(self):
        self.state = self.state_changes[self.state]

    def process_rows(self,row_index:int, sheet:Sheet):
        values = sheet.row_values(row_index)
        if values == ['']*len(values):
            self.state_process()

    @changes_state
    def process_schema(self, row_index:int, sheet:Sheet):
        self.schema = sheet.cell(row_index,0).value

    @changes_state
    def process_table(self, row_index:int, sheet:Sheet):
        self.table = sheet.cell(row_index,0).value

    @changes_state
    def process_cols(self, row_index:int, sheet:Sheet):
        pass


class Table:
    pass


if __name__ == "__main__":
    book = open_workbook('foo.xls')
    processed_sheets = []
    for sheet in book.sheets():
        processed_sheets.append(SheetReader(sheet))
    print(len(processed_sheets))