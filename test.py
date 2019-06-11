import sqlite3
from model import User
from schema import build_user

build_user()

mike = User(**{
    "username": "mikebloom",
    "password": "password",
    "realname": "Mike Bloom",
    "balance": 10000.0
})

assert mike.password == "password"
assert mike.pk is None

mike.save()

user1 = User.frompk(1)

assert user1.username == "mikebloom"

user2 = User.frompk(2)

assert user2 is None

mike.password = "12345"
mike.save()

mikeagain = User.frompk(1)

assert mikeagain.password == "12345"

print("tests passed")
