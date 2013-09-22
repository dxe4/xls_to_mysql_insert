__author__ = 'foobar'
from xlrd import open_workbook
from xlrd.sheet import Sheet
import sys

class SheetReader(object):
    state_changes = {
        "schema": "table",
        "table": "cols",
        "cols": "rows",
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
        self.process_sheet(sheet)
        self.add_table()

    def changes_state(f):
        def wrapper(*args):
            ret = f(*args)
            args[0].state_process()
            return ret

        return wrapper

    def process_sheet(self, sheet:Sheet):
        for row_index in range(sheet.nrows):
            self.process(row_index, sheet)

    def process(self, row_index, sheet:Sheet):
        callback = self.state_callbacks[self.state]
        callback(row_index, sheet)

    def state_process(self):
        self.state = self.state_changes[self.state]

    def fix_floats(self, values):
        return [self.fix_float(value) for value in values]

    def fix_float(self, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, float):
            str_value = str(value)
            if str_value.endswith(".0"):
                return str(int(value))
            else:
                return str_value


    def process_row(self, row_index:int, sheet:Sheet):
        values = sheet.row_values(row_index)
        values = self.fix_floats(values)
        if values == [''] * len(values):
            self.add_table()
            self.state_process()
        else:
            self.current_table.add_row(values)

    @changes_state
    def process_schema(self, row_index:int, sheet:Sheet):
        self.schema = sheet.cell(row_index, 0).value

    @changes_state
    def process_table(self, row_index:int, sheet:Sheet):
        self.current_table_name = sheet.cell(row_index, 0).value
        self.current_table = Table(self.schema, self.current_table_name, [], [])

    @changes_state
    def process_cols(self, row_index:int, sheet:Sheet):
        self.current_table.cols = sheet.row_values(row_index)


    def add_table(self):
        if self.current_table:
            self.tables.append(self.current_table)
            self.current_table = None


class Table:
    def __init__(self, schema:str, table:str, cols:list, rows:list):
        self.schema = schema
        self.table = table
        self.cols = cols
        self.rows = rows
        self.max_dict = {}
        self.extra_column_spaces = " "

    def add_row(self, row):
        self.rows.append(["NULL" if not i else i for i in row])

    def max_size_for_cols(self):
        #black magic :*(
        values_by_col = [
            (col_index, row[col_index])
            for row in self.rows + [self.cols]
            for col_index in range(0, len(self.cols))
        ]
        for col_index in range(0, len(self.cols)):
            filtered_by_col = filter(lambda arg: arg[0] == col_index, values_by_col)
            max_tuple = max(filtered_by_col, key=lambda l: len(l[1]))
            self.max_dict[max_tuple[0]] = len(max_tuple[1] + self.extra_column_spaces)


    def row_to_str(self, row):
        #black magic :*(

        def add_quotes(string:str):
            if string.endswith(")"):
                return string + "  "
            return "'" + string + "'"
        ret_str = "".join(
            [add_quotes(str(k)) +
             "".join(
                 (self.max_dict[i] - len(k)) * [" "]
             ) + "," for i, k in enumerate(row)
            ]
        )[:-1]


        return "(%s)\n" % ret_str


    def __str__(self):
        self.max_size_for_cols()
        insert = "INSERT INTO `%s`.`%s`" % (self.schema, self.table)
        columns = "\n" + self.row_to_str(self.cols)
        values = "VALUES"
        rows = "\n" + "".join([self.row_to_str(row) for row in self.rows])
        self.max_size_for_cols()

        return "".join([insert, columns, values, rows,";"])

    def __repr__(self):
        return "%s %s %s %s" % (self.schema, self.table, self.cols, self.rows)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No file name given")
        sys.exit()
    print(sys.argv[1])
    book = open_workbook(sys.argv[1])
    processed_sheets = []
    for sheet in book.sheets():
        processed_sheets.append(SheetReader(sheet))

    for sheet in processed_sheets:

        for table in sheet.tables:
            out_file = open("".join([table.schema,"-",table.table,".sql"]), "wt")
            out_file.write(str(table))
            out_file.close()