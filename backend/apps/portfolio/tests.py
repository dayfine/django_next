from django.test import TestCase

class ReallySimpleTest(TestCase):
    def test_one_plus_one_equals_two(self):
        self.assertEqual(1+1, 2)