from django.test import TestCase

# Create your tests here.
class BaseTest(TestCase):
    def test_assert_equal(self):
        """
        Test of assert True == True.
        Is only for demonstration purpouses.
        """
        self.assertEqual(True, True)
