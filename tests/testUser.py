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
        mike = User.from_pk(1)
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
        mike = User.from_pk(1)
        oldpk = mike.pk

        mike.balance = 0.0
        mike.save()

        self.assertEqual(mike.pk, oldpk,
            "pk does not change after save of exisiting row")

        mikeagain = User.from_pk(1)
        self.assertAlmostEqual(mikeagain.balance, 0.0,
            "updated properties saved to database and reloaded")
    
    def testOneWhere(self):
        mike = User.one_where("username=?",('mikebloom',))

        self.assertIsNotNone(mike, "Query does not return None when row is found")
        self.assertEqual(mike.password,'password',"object return has right properties")

    def testLogin(self):
        notauser= User.login('fuck','fuck')
        self.assertIsNone(notauser, "bad credentials retrun the None object")
    
        mike= User.login("mikebloom", "password")
        self.assertEqual(mike.realname,"Mike Bloom", "good credentials retrieve User Object")
    
    def testManyWhere(self):
        mike = User.many_where('username=?', ('mikebloom',))
        self.assertIsInstance(mike, list, " many where returns a list")
        self.assertEqual(len(mike),1, "List is one element")
        self.assertEqual(mike[0].password,'password', "checks user element")
        
    def testAll(self):
        mike = User.all()
        self.assertIsNotNone(mike, "Query does not return None when row is found")
        self.assertIs(type(mike), list, "A list was returned")
        
    def testDelete(self):
        mike = User.from_pk(1)
        mike.delete()
        self.assertIsNone(mike.pk,".delete should set pk to None")
        secondmike = User.from_pk(1)
        self.assertIsNone(secondmike,".delete removes row from db")