

# Import necessary modules
import pickle
import uuid
from abc import ABC, abstractmethod

# Abstract base class for all users
class User(ABC):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @abstractmethod
    def login(self, email, password):
        pass

# Customer class
class Customer(User):
    def __init__(self, username, email, password):
        super().__init__(username, email, password)
        self.purchase_history = []  # list of Order objects

    def login(self, email, password):
        return self.email == email and self.password == password

    def create_account(self):
        save_data('customers.pkl', self)

    def update_account(self, new_email=None, new_password=None):
        if new_email:
            self.email = new_email
        if new_password:
            self.password = new_password

    def view_order_history(self):
        return self.purchase_history

# Admin class
class Admin(User):
    def __init__(self, username, email, password):
        super().__init__(username, email, password)

    def login(self, email, password):
        return self.email == email and self.password == password

    def view_sales_report(self):
        return load_data('sales.pkl')

    def modify_discounts(self):
        pass  # Placeholder

# Abstract base class for all ticket types
class Ticket(ABC):
    def __init__(self, price):
        self.ticket_id = str(uuid.uuid4())  # unique ID
        self.price = price

    @abstractmethod
    def get_price(self):
        pass

# Specific ticket types
class SingleRaceTicket(Ticket):
    def get_price(self):
        return self.price

class WeekendPackage(Ticket):
    def get_price(self):
        return self.price * 0.9  # 10% off

class SeasonMembership(Ticket):
    def get_price(self):
        return self.price * 0.8  # 20% off

class GroupDiscountTicket(Ticket):
    def get_price(self):
        return self.price * 0.75  # 25% off

# Order class
class Order:
    def __init__(self, customer, tickets):
        self.order_id = str(uuid.uuid4())
        self.customer = customer
        self.tickets = tickets
        self.total_price = self.calculate_total()

    def calculate_total(self):
        return sum(ticket.get_price() for ticket in self.tickets)

# Payment class
class Payment:
    def __init__(self, method, amount):
        self.payment_method = method
        self.amount = amount

    def process_payment(self):
        return True  # Assume payment success

# Ticket Manager to track ticket availability and sales
class TicketManager:
    def __init__(self):
        self.sales = []  # list of Order

    def sell_ticket(self, customer, tickets):
        order = Order(customer, tickets)
        customer.purchase_history.append(order)
        self.sales.append(order)
        save_data('sales.pkl', self.sales)
        return order

# Helper functions to save/load data

def save_data(filename, data):
    try:
        existing_data = []
        try:
            with open(filename, 'rb') as file:
                existing_data = pickle.load(file)
        except FileNotFoundError:
            pass
        existing_data.append(data)
        with open(filename, 'wb') as file:
            pickle.dump(existing_data, file)
    except Exception as e:
        print(f"Error saving data: {e}")

def load_data(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

# Simple test case
def test():
    c1 = Customer('john_doe', 'john@example.com', '1234')
    c1.create_account()
    t1 = SingleRaceTicket(150.0)
    t2 = WeekendPackage(300.0)
    tm = TicketManager()
    order = tm.sell_ticket(c1, [t1, t2])
    print(f"Order total: ${order.total_price:.2f}")

test()
