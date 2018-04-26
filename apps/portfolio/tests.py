from django.test import TestCase


# django1.8.18 - benchmark under python3 venv: 7~11s
# django1.9.13 - normal: ~9s
# django1.9.13 - parallel=4: 4-6s


class ReallySimpleTest(TestCase):
    def test_one_plus_one_equals_two(self):
        for i in range(1, 1000000):
            self.assertEqual(i*i+2*i+1, (i+1)**2)
            self.assertEqual(i/(i/2), 2)


class SomewhatSimpleTest(TestCase):
    def test_one_plus_one_equals_two(self):
        for i in range(1, 1000000):
            self.assertEqual(i*i+2*i+1, (i+1)**2)
            self.assertEqual(i/(i/2), 2)


class SimplerTest(TestCase):
    def test_one_plus_one_equals_two(self):
        for i in range(1, 1000000):
            self.assertEqual(i*i+2*i+1, (i+1)**2)
            self.assertEqual(i/(i/2), 2)
