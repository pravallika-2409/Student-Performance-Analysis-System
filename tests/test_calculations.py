import unittest
from utils.calculations import calculate_percentage, calculate_grade, pass_or_fail

class CalculationTests(unittest.TestCase):
    def test_percentage(self):
        self.assertEqual(calculate_percentage(45, 50), 90.0)

    def test_invalid_marks(self):
        with self.assertRaises(ValueError):
            calculate_percentage(60, 50)

    def test_grade(self):
        self.assertEqual(calculate_grade(91), "A+")
        self.assertEqual(calculate_grade(39), "F")

    def test_pass_fail(self):
        self.assertEqual(pass_or_fail(40, 40), "Pass")
        self.assertEqual(pass_or_fail(39, 40), "Fail")

if __name__ == "__main__":
    unittest.main()
