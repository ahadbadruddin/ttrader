
def create_insert(tablename, columns):
    # firstname, lastname, employee_id
    columnlist = ", ".join(columns)
    qmarks = ", ".join("?" for val in columns)
    SQL = """ INSERT INTO {tablename} ({columnlist})
    VALUES ({qmarks}) """
    return SQL.format(tablename=tablename, columnlist=columnlist, qmarks=qmarks)

if __name__ == "__main__":
    print(create_insert('employees', ['firstname', 'lastname', 'employee_id', 'birth_date']))