import unittest
from main import check_login
class TestLogin(unittest.TestCase):
    def test_correct_cred(self):
        self.assertTrue(check_login("Malika","MALIKA COOL"))

    def test_wrong_username(self):
        self.assertFalse(check_login("wrongUser","MALIKA COOL"))

    def test_wrong_password(self):
        self.assertFalse(check_login("Malika","wrongpass"))

    def test_both_wrong(self):
        self.assertFalse(check_login("WrongUser","wrongpass"))

if __name__=="__main__":
    unittest.main()