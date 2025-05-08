
import tkinter as tk # Imports the tkinter module for GUI creation
from tkinter import ttk, messagebox  # Imports themed widgets (ttk) and messagebox for pop-up dialogs
from models import * # Imports all classes and functions from the 'models' module

class LoginScreen: # Defines a class for the login screen GUI
    def __init__(self, root, on_login):# Constructor takes the main window (root) and a callback function on successful login
        self.root = root  # Stores the root window
        self.on_login = on_login # Stores the login callback function
        
        self.frame = ttk.Frame(root, padding="20")# Creates a frame with padding inside the root window
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))# Places the frame in the grid and makes it stretch in all directions
        
        ttk.Label(self.frame, text="Email:").grid(row=0, column=0, pady=5)# Adds a label for the email field in the first row
        self.email_entry = ttk.Entry(self.frame)# Creates an entry widget for email input
        self.email_entry.grid(row=0, column=1, pady=5)# Places the email entry to the right of the label
        
        ttk.Label(self.frame, text="Password:").grid(row=1, column=0, pady=5) # Adds a label for the password field
        self.password_entry = ttk.Entry(self.frame, show="*")# Creates an entry widget for password input, masks the characters
        self.password_entry.grid(row=1, column=1, pady=5)# Places the password entry to the right of the label
        
        ttk.Button(self.frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
         # Adds a "Login" button that calls self.login when clicked; spans two columns
        ttk.Button(self.frame, text="Register", command=self.show_register).grid(row=3, column=0, columnspan=2)
         # Adds a "Register" button that calls self.show_register when clicked; also spans two columns
    def login(self): # Defines the login function triggered when the "Login" button is clicked
        email = self.email_entry.get()# Gets the entered email from the email entry field
        password = self.password_entry.get() # Gets the entered password from the password entry field
        users = DataManager.load_data("users.pkl")# Loads the list of users from the 'users.pkl' file using the DataManager
        
        for user in users:# Iterates over all users to check credentials
            if user.email == email and user.authenticate(password): #If email matches and password is correct
                self.on_login(user)# Calls the callback function with the logged-in user
                return # Exits the login function
        messagebox.showerror("Error", "Invalid credentials!")  # Shows an error message if login fails
