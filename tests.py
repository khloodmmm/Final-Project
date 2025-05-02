import unittest
from models import *

class TestModels(unittest.TestCase):
    def setUp(self):
        self.customer = Customer(1, "Alice", "alice@example.com", "pass123")
        self.ticket = Ticket(1, TicketType.SINGLE, 100, "2023-11-20")

    def test_customer_creation(self):
        self.assertEqual(self.customer.name, "Alice")

    def test_order_total(self):
        order = Order(1, 1, [self.ticket], 0.1)
        self.assertEqual(order.total, 90)  # 10% discount

if __name__ == "__main__":
    unittest.main()
