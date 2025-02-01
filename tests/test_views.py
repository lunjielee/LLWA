from django.test import TestCase
from restaurant.models import Menu

class MenuViewTest(TestCase):
    def setUp(self):
        self.item1 = Menu.objects.create(name='first', price=1)
        self.item2 = Menu.objects.create(name='second', price=2)

    def test_getall(self):
        first = Menu.objects.get(name='first')
        second = Menu.objects.get(name='second')

        self.assertEqual(str(first), 'first : 1')
        self.assertEqual(str(second), 'second : 2')