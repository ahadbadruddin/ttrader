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
        update_column_list = ", ".join(fields + "=?" for fields in cls.fields)
        SQL = """
             UPDATE {tablename} SET {update_column_list} WHERE pk = ?;"""
        return SQL.format(tablename=cls.dbtable, update_column_list=update_column_list)

    
    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = self._create_update()
            propvals = [getattr(self, propname) for propname in self.fields + ["pk"]]
            cur.execute(SQL, propvals)    
        
    @classmethod
    def one_where(cls, whereclause, values):
        SQL = f"SELECT * FROM {cls.dbtable} WHERE " + whereclause
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute(SQL,values)
            row = cur.fetchone()
            if row is None:
                return None
            return cls(**row)
        
    @classmethod
    def many_where(cls,whereclause="TRUE", values=tuple()):
        """ equivalent of one where but with fetch allm retunrs a listr of obkects or an empty list"""
        SQL = f"SELECT * FROM {cls.dbtable} WHERE " + whereclause
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, values)
            rows = cur.fetchall()
            return [cls(**row) for row in rows]

    @classmethod
    def from_pk(cls,pk):
        return cls.one_where("pk=?",(pk,))

    @classmethod
    def all(cls):
        """ return a list of every row in the table as instance of the class"""
        return cls.many_where()

    def delete(self):
        SQL= f"DELETE FROM {self.dbtable} WHERE pk= ?"
        with sqlite3.connect(self.dbpath) as conn:
            cur= conn.cursor()
            cur.execute(SQL,(self.pk,))
            self.pk= None

    def __repr__(self):
        reprstring = "<{cname} {fieldvals}>"
        fieldvals = " ".join("{key}:{value}".format(key = key, value= getattr(self, key))
                                for key in ["pk",*self.fields])
        cname = type(self).__name__
        return reprstring.format(cname= cname, fieldvals= fieldvals)

