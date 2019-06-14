from model.user import User
from model.position import Position
from unittest import TestCase
from schema import build_user, build_positions

# to execute from the base of the prokect directory structure run:
# python3 -m unittest tests/testPosition.py
# to run all tests in directory run:
# python3 -m unnit
class TestUser(TestCase):

    def setUp(self):
        build_user()
        build_positions()

        mike = User(**{
             "username": "mikebloom",
             "realname": "Mike Bloom",
             "balance": 10000.0
        })
        mike.hash_password("password")
        mike.save()

        appl = Position(**{
            "ticker" : "AAPL",
            "amount": 5,
            "user_info_pk": mike.pk
        })

        tsla = Position(**{
            "ticker" : "TSLA",
            "amount": 10,
            "user_info_pk": mike.pk
        })

        appl.save()
        tsla.save()

    def tearDown(self):
        pass

    def testDummy(self):
        pass
    
    def testOneWhere(self):
        pass
    
    def testSave(self):
        pass
    
    def testAllPositions(self):
        mike= User.from_pk(1)
        positions = mike.all_positions()
        self.assertIsInstance(positions, list, ".all_positions returns a list")
        firstposition = positions[0]
        self.assertIsInstance(firstposition,Position,"checks to see if it is position object")

    def testOnePositions(self):
        mike = User.from_pk(1)
        position= mike.positions_for_stock("AAPL")
        self.assertIsInstance(position, Position, "checks to see if it a position object")
    

    