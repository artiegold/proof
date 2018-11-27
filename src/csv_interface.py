import csv
"""Extract information from a standard CSV file."""
class ColumnNameException(Exception):
    """Exception thrown when needed columns are missing form the CSV"""
    pass

class TableNameException(Exception):
    """Exception thrown when specified table name from CSV does not match"""
    pass

class Extract_CSV_Info:
    """
    Extract information from a csv file

    Constructor arguments:
        file_name:          string containing name of the file
        expected_columns:   list of column names we are interested in
        expected_table_name (optional): Check table name of input if supplied
    """
    def __init__(self, file_name, expected_columns, expected_table_name=None):
        """Constructor."""
        self.file_name = file_name
        self.expected_columns = expected_columns
        self.expected_table_name = expected_table_name

    @staticmethod
    def get_headers(input_file):
        """Retrieves table name and column names from CSV file."""
        reader = csv.reader(input_file)
        i = 0
        for line in reader:
            if i == 0:
                table_name = line[0]
            elif i == 1:
                pass # nothing to do
            elif i == 2:
                column_names = [name.strip() for name in line if name != '']
                break

            i += 1
        return table_name, column_names

    def valid(self, d):
        """Validates line. Invalid lines will be ignored."""
        for k,v in d.iteritems():
            if k in self.expected_columns and v == '':
                return False
        return True

    @staticmethod
    def stripped(line):
        return dict((k, v.strip()) for k, v in line.iteritems())

    def get_lines(self, input_file, column_names):
        """Yields valid lines from input."""
        reader = csv.DictReader(input_file, column_names)
        for line in reader:
            del line[None]
            if self.valid(line):
                yield Extract_CSV_Info.stripped(line)

    def check_columns(self, column_names):
        """Verifies expected columns are present. Throws ColumnNameException otherwise."""
        expected_set = set(self.expected_columns)
        actual_set = set(column_names)
        diff = expected_set.difference(actual_set)
        if len(diff) != 0:
            raise ColumnNameException(str(list(diff)) + ": fields not available")

    def check_table_name(self, table_name):
        """
        Verifies table name from CSV if expected_table_name has been specified. 
        Throws TableNameException on mismatch.
        """
        if self.expected_table_name is not None:
            if self.expected_table_name != table_name:
                raise TableNameException("Expected table: " + self.expected_table_name + ' got: ' + table_name)

    def read_input_file(self):
        """Manages input file. Checks headers. Supplies stream of valid lines."""
        with open(self.file_name, 'r') as input_file:
            table_name, column_names = Extract_CSV_Info.get_headers(input_file)
            self.check_columns(column_names)
            self.check_table_name(table_name)
            if not set(column_names).issubset(set(self.expected_columns)):
                raise ColumnNameException(str(set(self.expected_columns).difference()))

            for line in self.get_lines(input_file, column_names):
                yield line


# sanity check code
if __name__ == '__main__':
    reader = Extract_CSV_Info(
        'data/input/Proof_homework.csv',
        ['User ID', 'IP', 'Geo', 'Industry', 'Company Size']
    )
    for line in reader.read_input_file():
        print line
