from model.user import User
from unittest import TestCase
from schema import build_user

# to execute from the base of the prokect directory structure run:
# python3 -m unittest tests/testUser.py
# to run all tests in directory run:
# python3 -m unnit
class TestUser(TestCase):

    def setUp(self):
        build_user()

        mike = User(**{
             "username": "mikebloom",
             "password": "password",
             "realname": "Mike Bloom",
             "balance": 10000.0
        })

        mike.save()

    def tearDown(self):
        pass
    
    def testFromPk(self):
        mike = User.frompk(1)
        self.assertEqual(mike.realname, "Mike Bloom", 
        "Lookup from pk populates instance properties")
    
    def testSavePK(self):
        # test that pk is defined after a save
        greg = User(**{
            "username":"gregcoin",
            "realname":"Greg Smith",
            "balance": 200.0,
            "password": "12345"
        })
        self.assertIsNone(greg.pk,"pk value of the new instance initializes to None")

        greg.save()

        self.assertGreater(greg.pk, 1,
        "pk is set after first save")

    def testSaveUpdate(self):
        mike = User.frompk(1)
        oldpk = mike.pk

        mike.balance = 0.0
        mike.save()

        self.assertEqual(mike.pk, oldpk,
            "pk does not change after save of exisiting row")

        mikeagain = User.frompk(1)
        self.assertAlmostEqual(mikeagain.balance, 0.0,
            "updated properties saved to database and reloaded")

        