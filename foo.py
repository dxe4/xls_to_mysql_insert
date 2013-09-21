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
            "rows": self.process_row,
            "cols": self.process_cols
        }
        self.current_table_name = None
        self.current_table = None
        self.tables = []
        self.rows = []
        self.cols = []
        self.process_sheet(sheet)
        self.add_table()
        print(self.schema, "  ", self.current_table_name)

    def changes_state(f):
        def wrapper(*args):
            ret =  f(*args)
            args[0].state_process()
            return ret
        return wrapper

    def process_sheet(self, sheet:Sheet):
        print(" rows ", sheet.nrows, " cols ", sheet.ncols)
        for row_index in range(sheet.nrows):
            self.process(row_index, sheet)

    def process(self, row_index, sheet:Sheet):
        print(self.state)
        callback = self.state_callbacks[self.state]
        callback(row_index, sheet)

    def state_process(self):
        self.state = self.state_changes[self.state]

    def process_row(self,row_index:int, sheet:Sheet):
        values = sheet.row_values(row_index)
        if values == ['']*len(values):
            self.add_table()
            self.state_process()
        else:
            self.current_table.rows.append(values)

    @changes_state
    def process_schema(self, row_index:int, sheet:Sheet):
        self.schema = sheet.cell(row_index,0).value

    @changes_state
    def process_table(self, row_index:int, sheet:Sheet):
        self.current_table_name = sheet.cell(row_index,0).value
        self.current_table = Table(self.schema,self.current_table_name,[],[])
        self.clear_state()

    @changes_state
    def process_cols(self, row_index:int, sheet:Sheet):
        self.current_table.cols = sheet.row_values(row_index)

    def clear_state(self):
        self.cols = []
        self.rows = []

    def add_table(self):
        if self.current_table:
            self.tables.append(self.current_table)
            self.current_table = None


class Table:
    def __init__(self,schema:str,table:str,cols:list,rows:list):
        self.schema = schema
        self.table = table
        self.cols = cols
        self.rows = rows

    def __str__(self):
        return "%s %s %s %s" % (self.schema,self.table,self.cols,self.rows)

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    book = open_workbook('foo.xls')
    processed_sheets = []
    for sheet in book.sheets():
        processed_sheets.append(SheetReader(sheet))
    print(len(processed_sheets))
    for s in processed_sheets:
        print(str(s.tables))