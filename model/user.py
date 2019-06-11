import sqlite3
from .orm import Sqlite3ORM

#DBNAME="trader.db"
#TABLENAME="user_info"

class User(Sqlite3ORM):
    fields = ['username', 'password', 'realname', 'balance']
    dbtable = "user_info"
    dbpath = "trader.db"

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.realname = kwargs.get('realname')
        self.balance = kwargs.get('balance', 0.0)

    @classmethod
    def login(cls, username, password):
        return cls.one_where("username= ? AND password= ?",(username, password))