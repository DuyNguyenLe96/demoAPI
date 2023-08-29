from django.test import TestCase
from .models import UserModel


# Create your tests here.
class MyTestCase(TestCase):
    def test_case_user(self):
        a = UserModel.objects.create(first_name='ma', email='dft@gmail.com', password='darklorD@12')
        self.assertEqual(a.password, 'darklorD@12')
