import unittest
import legacy_order_system as legacy
import refactored_order_system as refactored


class TestOrderSystemRegression(unittest.TestCase):

    def setUp(self):
        # Base basket: (2 * 300) + (1 * 800) = 1400 PKR subtotal
        self.sample_items = [
            {'name': 'Notebook', 'category': 'book', 'price': 300, 'qty': 2},
            {'name': 'USB Drive', 'category': 'electronics', 'price': 800, 'qty': 1},
        ]

    def test_1_regular_customer_standard_delivery(self):
        """Regular customer (0% discount) with standard delivery (+100 PKR)."""
        before = legacy.order_total(self.sample_items, 'regular', 'standard')
        after = refactored.order_total(self.sample_items, 'regular', 'standard')
        self.assertEqual(before, 1500.0)
        self.assertEqual(before, after)

    def test_2_student_discount(self):
        """Student customer (10% discount -> 1260 PKR) with standard delivery (+100 PKR)."""
        before = legacy.order_total(self.sample_items, 'student', 'standard')
        after = refactored.order_total(self.sample_items, 'student', 'standard')
        self.assertEqual(before, 1360.0)
        self.assertEqual(before, after)

    def test_3_staff_discount(self):
        """Staff customer (5% discount -> 1330 PKR) with standard delivery (+100 PKR)."""
        before = legacy.order_total(self.sample_items, 'staff', 'standard')
        after = refactored.order_total(self.sample_items, 'staff', 'standard')
        self.assertEqual(before, 1430.0)
        self.assertEqual(before, after)

    def test_4_standard_delivery_only(self):
        """Standard delivery fee verification (+100 PKR) with no discount."""
        items = [{'name': 'Pen', 'category': 'stationery', 'price': 100, 'qty': 1}]
        before = legacy.order_total(items, 'regular', 'standard')
        after = refactored.order_total(items, 'regular', 'standard')
        self.assertEqual(before, 200.0)
        self.assertEqual(before, after)

    def test_5_express_delivery(self):
        """Express delivery fee verification (+250 PKR) with student discount."""
        before = legacy.order_total(self.sample_items, 'student', 'express')
        after = refactored.order_total(self.sample_items, 'student', 'express')
        self.assertEqual(before, 1510.0)
        self.assertEqual(before, after)

    def test_6_invalid_negative_input_raises_value_error(self):
        """Negative price or quantity must raise ValueError in refactored code."""
        invalid_price_items = [{'name': 'Faulty Book', 'category': 'book', 'price': -300, 'qty': 1}]
        invalid_qty_items = [{'name': 'USB Drive', 'category': 'electronics', 'price': 800, 'qty': -2}]

        with self.assertRaises(ValueError):
            refactored.order_total(invalid_price_items, 'regular', 'standard')

        with self.assertRaises(ValueError):
            refactored.order_total(invalid_qty_items, 'student', 'express')


if __name__ == '__main__':
    unittest.main(verbosity=2)