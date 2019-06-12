import sqlite3
from .orm import Sqlite3ORM

#DBNAME="trader.db"
#TABLENAME="user_info"

class User(Sqlite3ORM):
    fields = ['username', 'password', 'realname', 'balance']
    dbtable = "user_info"
    dbpath = "trader.db"

    def __init__(self, **kwargs): #kwargs turns given parameter of list into a dictionary
        self.pk = kwargs.get('pk')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.realname = kwargs.get('realname')
        self.balance = kwargs.get('balance', 0.0)

    def hash_password(self,password):
        """ someuser.hashpassword ("somepassword") sets someuser's self.password
        to a bcrypt encoded hash"""


    @classmethod
    def login(cls, username, password):
        """ search for the user with the given username (use one_where) and then use 
        bcrypt's checkpw() to verify that the credentials are correct 
        return None for bad credentials or the mathing USer instance on a successful login"""

        #return cls.one_where("username= ? AND password= ?",(username, password))

    