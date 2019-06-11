import sqlite3

class Sqlite3ORM:
    fields = []
    dbpath = ""
    dbtable = ""
    create = ""

    def __init__(self):
        raise NotImplementedError

    @classmethod   
    def _create_insert(cls):
        columnlist = ", ".join(cls.fields)
        qmarks = ", ".join("?" for val in cls.fields)
        SQL = """ INSERT INTO {tablename} ({columnlist})
    VALUES ({qmarks}) """
        return SQL.format(tablename=cls.dbtable, columnlist=columnlist, qmarks=qmarks)

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = self._create_insert()
            propvals= [getattr(self, propname) for propname in self.fields]
            cur.execute(SQL, propvals)
            self.pk = cur.lastrowid

    def save(self):
        if self.pk is None:
            self._insert()
        else:
            self._update()

    @classmethod
    def _create_update(cls):
        cls.fields[-1] += "=?"
        update_column_list = "=?, ".join(cls.fields)
        SQL = """
             UPDATE {tablename} SET {update_column_list} WHERE pk = ?;"""
        return SQL.format(tablename=cls.dbtable, update_column_list=update_column_list)

    
    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = self._create_insert()
            propvals = [getattr(self, propname) for propname in self.fields + [self.pk]]
            cur.execute(SQL, propvals)    
