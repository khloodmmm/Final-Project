# Import necessary libraries
import tkinter as tk # GUI library
from tkinter import ttk, messagebox  # ttk for themed widgets, messagebox for popup dialogs
from enum import Enum # For defining enumerated constants
from datetime import datetime  # For working with dates and times
import pickle # For saving/loading objects to/from files
from typing import List, Optional # For type annotations

# Define an enumeration for different ticket types with descriptions and pricing
class TicketType(Enum):
    SINGLE_RACE = "Single Race Pass(100$), Valid for 1 race day only, It access to one Grand Prix race "
    WEEKEND = "Weekend Package(250$), Valid from Fridat to Saturaday, It has access to all race weekned events"
    SEASON = "Season Membership(1000$),Valid for entire race season, It has access to all races and exclusive merchandise"
    GROUP = "Group Package(80$), Valid for 1 race day for 4 people, I t has free drinks for each one "

#class representing a user
class User:
    def __init__(self, id: int, name: str, email: str, password: str):
        self._id = id
        self._name = name # User's name
        self._email = email # User's email address
        self._password = password # User's password 

    # Getter for user ID
    @property
    def id(self) -> int:
        return self._id
    
    # Getter for user name
    @property
    def name(self) -> str:
        return self._name

    # Getter for user email
    @property
    def email(self) -> str:
        return self._email

    #check if a given password matches the user's password
    def authenticate(self, password: str) -> bool:
        return self._password == password
# Class representing an admin user, inherits from User
class Admin(User):
    def __init__(self, id: int, name: str, email: str, password: str):
        super().__init__(id, name, email, password)# Initialize parent User attributes
        self._is_admin = True # Flag indicating this user is an admin

    # Getter for admin status
    @property
    def is_admin(self) -> bool:
        return self._is_admin
# Class representing a customer user, inherits from User
class Customer(User):
    def __init__(self, id: int, name: str, email: str, password: str):
        super().__init__(id, name, email, password) # Initialize parent User attributes
        self._purchase_history: List[Order] = [] # List to store customer's order history
        self._loyalty_points = 0 # Customer's loyalty points

    # Getter for purchase history
    @property
    def purchase_history(self) -> List['Order']:
        return self._purchase_history

    # Getter for loyalty points
    @property
    def loyalty_points(self) -> int:
        return self._loyalty_points

    # Setter for loyalty points
    @loyalty_points.setter
    def loyalty_points(self, points: int):
        self._loyalty_points = points

# Class representing a ticket
class Ticket:
    def __init__(self, id: int, type: TicketType, price: float, event_date: str):
        self._id = id
        self._type = type # Type of ticket (enum)
        self._price = price # Ticket price
        self._event_date = event_date # Date of the event
        self._is_valid = True  # Validity status of the ticket
    # Getter for ticket ID
    @property
    def id(self) -> int:
        return self._id

    # Getter for ticket type
    @property
    def type(self) -> TicketType:
        return self._type

    # Getter for ticket price
    @property
    def price(self) -> float:
        return self._price

    # Getter for event date
    @property
    def event_date(self) -> str:
        return self._event_date

    # Getter for ticket validity
    @property
    def is_valid(self) -> bool:
        return self._is_valid

    # Setter for ticket validity
    @is_valid.setter
    def is_valid(self, value: bool):
        self._is_valid = value

# Class representing an order made by a customer
class Order:
    def __init__(self, id: int, customer_id: int, tickets: List[Ticket], payment_method: str):
        self._id = id
        self._customer_id = customer_id
        self._tickets = tickets # List of tickets in the order
        self._payment_method = payment_method # Payment method used
        self._order_date = datetime.now() # Date and time when the order was placed
        self._status = "Pending" # Current status of the order
        self._discount = 0 # Discount applied to the order

    # Getter for order ID
    @property
    def id(self) -> int:
        return self._id

    # Getter for customer ID
    @property
    def customer_id(self) -> int:
        return self._customer_id
    
    # Getter for ticket list
    @property
    def tickets(self) -> List[Ticket]:
        return self._tickets
    
    # Getter for payment method
    @property
    def payment_method(self) -> str:
        return self._payment_method

    # Getter for order date
    @property
    def order_date(self) -> datetime:
        return self._order_date

    # Getter for order status
    @property
    def status(self) -> str:
        return self._status

    # Setter for order status
    @status.setter
    def status(self, value: str):
        self._status = value

    # Getter for discount
    @property
    def discount(self) -> float:
        return self._discount

    #Setter for discount
    @discount.setter
    def discount(self, value: float):
        self._discount = value

    #Property to calculate the total amount after applying discount
    @property
    def total(self) -> float:
        subtotal = sum(ticket.price for ticket in self.tickets)
        return subtotal * (1 - self.discount)  # Apply discount and return final total
    
# Class to manage saving and loading of data to/from files
class DataManager:
    # Method to save any data object to a file using pickle
    @staticmethod
    def save_data(data: any, filename: str) -> None:
        with open(filename, 'wb') as file: #open file in binary write mode
            pickle.dump(data, file) # Serialize and save the data

     # Method to load any data object from a file using pickle
    @staticmethod
    def load_data(filename: str) -> any:
        try:
            with open(filename, 'rb') as file: # Open file in binary read mode
                return pickle.load(file) # Load and return the serialized data
        except FileNotFoundError:
            return [] # If file doesn't exist, return an empty list

