import sqlite3
from .orm import Sqlite3ORM
import bcrypt
from model.position import Position
from .util import get_price

#DBNAME="trader.db"
#TABLENAME="user_info"



class InsufficientFundsError(Exception):
    pass

class InsufficientSharesError(Exception):
    pass


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

    def hash_password(self,plain_text_pw):
        """ someuser.hashpassword ("somepassword") sets someuser's self.password
        to a bcrypt encoded hash"""
        self.password = bcrypt.hashpw(plain_text_pw.encode(), bcrypt.gensalt())


    @classmethod
    def login(cls, username, plain_text_pw):
        """ search for the user with the given username (use one_where) and then use 
        bcrypt's checkpw() to verify that the credentials are correct 
        return None for bad credentials or the mathing USer instance on a successful login"""
        user = cls.one_where("username=?", (username,))
        if user is None:
            return None
        if bcrypt.checkpw(plain_text_pw.encode(), user.password):
            return user
        return None

    def all_positions(self):
        positions = Position.many_where("user_info_pk=?",(self.pk,))
        return positions

    def positions_for_stock(self,ticker):
        position = Position.one_where("user_info_pk=? AND ticker=?",(self.pk,ticker.upper()))
        return position

    def buy(self, ticker, amount):
        #TODO make a trade
        """ buy a stock. if there is no current position, create one, if there is
        increase its amount. no return value """
        if amount < 0:
            raise ValueError
        cost = get_price(ticker)* amount
        if self.balance < cost:
            raise InsufficientFundsError
        self.balance -= cost
        current_position = self.position_for_stock(ticker)
        if current_position is None:
            current_position = Position(ticker=ticker, amount=0, user_info_pk=self.pk)
        current_position.amount += amount
        current_position.save()
        self.save

    def sell(self,ticker, amount):
        #TODO, make a trade (volume )
        if amount < 0:
            raise ValueError
        cost = get_price(ticker)* amount
        position = self.positions_for_stock(ticker)
        if position is None or amount > position.amount:
            raise InsufficientSharesError
        position.amount -= amount
        self.balance += cost
        position.save()
        self.save()
    
    def all_trades(self):
        """return a list of trade objects for every trade made by this user
         arranged oldest to newest"""
    
    def 
        