import pickle
from enum import Enum, auto
from datetime import datetime
import os

# Enums for ticket types and payment methods
class TicketType(Enum):
    SINGLE = "Single Race Pass"
    WEEKEND = "Weekend Package"
    SEASON = "Season Membership"

class PaymentMethod(Enum):
    CREDIT = "Credit Card"
    DEBIT = "Debit Card"
    WALLET = "Digital Wallet"

# User Class (Abstract)
class User:
    def __init__(self, user_id, name, email, password):
        self._user_id = user_id
        self.name = name
        self.email = email
        self._password = password  # In practice, hash this!

    def authenticate(self, password):
        return self._password == password

# Customer Class
class Customer(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self.orders = []

    def place_order(self, tickets, discount=0):
        order = Order(len(self.orders) + 1, self._user_id, tickets, discount)
        self.orders.append(order)
        return order

# Admin Class
class Admin(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)

    def update_discount(self, ticket_type, new_discount):
        # Logic to update discounts (stored separately)
        pass

# Ticket Class
class Ticket:
    def __init__(self, ticket_id, ticket_type, price, event_date):
        self.ticket_id = ticket_id
        self.type = ticket_type
        self.price = price
        self.event_date = event_date

# Order Class
class Order:
    def __init__(self, order_id, user_id, tickets, discount=0):
        self.order_id = order_id
        self.user_id = user_id
        self.tickets = tickets
        self.discount = discount
        self.total = sum(t.price for t in tickets) * (1 - discount)
        self.timestamp = datetime.now()

# File Operations
def save_data(data, filename):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{filename}", "wb") as f:
        pickle.dump(data, f)

def load_data(filename):
    try:
        with open(f"data/{filename}", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []  # Return empty list if file doesn't exist

# Initialize sample data
def init_sample_data():
    tickets = [
        Ticket(1, TicketType.SINGLE, 100, "2023-11-20"),
        Ticket(2, TicketType.WEEKEND, 250, "2023-11-25"),
    ]
    save_data(tickets, "tickets.pkl")
    save_data([], "users.pkl")
    save_data([], "orders.pkl")
