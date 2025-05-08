
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

    def show_register(self):# Defines the function to show the registration screen
        RegisterScreen(tk.Toplevel(self.root))# Opens the RegisterScreen in a new popup window (Toplevel)

class RegisterScreen:# Defines the registration screen class
    def __init__(self, root):# Constructor takes a window as input
        self.root = root # Stores the root window
        self.root.title("Register") # Sets the title of the window to "Register"
        
        frame = ttk.Frame(root, padding="20")# Creates a frame with padding
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))# Places the frame in the grid layout
        
        ttk.Label(frame, text="Name:").grid(row=0, column=0)# Adds a label for the name field
        self.name_entry = ttk.Entry(frame)# Creates an entry field for the user's name
        self.name_entry.grid(row=0, column=1)# Places the name entry to the right of the label
        
        ttk.Label(frame, text="Email:").grid(row=1, column=0)# Adds a label for the email field
        self.email_entry = ttk.Entry(frame)# Creates an entry field for the user's email
        self.email_entry.grid(row=1, column=1)# Places the email entry to the right of the label
        
        ttk.Label(frame, text="Password:").grid(row=2, column=0)# Adds a label for the password field
        self.password_entry = ttk.Entry(frame, show="*")# Creates an entry field for password, masked with "*"
        self.password_entry.grid(row=2, column=1)# Places the password entry to the right of the label
        
        ttk.Button(frame, text="Register", command=self.register).grid(row=3, column=0, columnspan=2)
         # Adds a "Register" button that calls self.register when clicked; spans two columns
    def register(self):# Defines the registration logic
        users = DataManager.load_data("users.pkl")# Loads existing users from the 'users.pkl' file
        new_id = len(users) + 1# Sets a new user ID based on the current number of users
          # Creates a new Customer object with the entered name, email, and password
        customer = Customer(new_id, self.name_entry.get(), self.email_entry.get(), self.password_entry.get())
        users.append(customer)# Adds the new customer to the list of users
        DataManager.save_data(users, "users.pkl")# Saves the updated user list back to the file
        messagebox.showinfo("Success", "Registration successful!")# Shows a success message
        self.root.destroy()# Closes the registration window

class TicketBookingScreen:
    def __init__(self, root, user):# Initializes the TicketBookingScreen with the main window and current user
        self.root = root # Stores the main tkinter window
        self.user = user # Stores the logged-in user object
        
        frame = ttk.Frame(root, padding="20")# Creates a main frame with padding inside the root window
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) # Places the frame using grid layout
        # Welcome message with the user's name
        ttk.Label(frame, text=f"Welcome, {user.name}!", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Ticket Selection
        ticket_frame = ttk.LabelFrame(frame, text="Select Ticket", padding="10")# A labeled section for ticket choices
        ticket_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")# Spans across two columns
        
        self.ticket_type = tk.StringVar() # Variable to hold selected ticket type
        ticket_types = [t.value for t in TicketType]# Gets list of ticket type values from the TicketType enum
        ttk.Label(ticket_frame, text="Ticket Type:").grid(row=0, column=0)# Label for ticket type selection
        ttk.Combobox(ticket_frame, textvariable=self.ticket_type, values=ticket_types).grid(row=0, column=1)# Dropdown for ticket type
        
        # Date Selection
        self.race_date = tk.StringVar()# Variable to store race date
        ttk.Label(ticket_frame, text="Race Date (YYYY-MM-DD):").grid(row=1, column=0)# Label for date input
        date_entry = ttk.Entry(ticket_frame, textvariable=self.race_date)# Entry field for race date
        date_entry.grid(row=1, column=1) # Places entry next to label
        date_entry.insert(0, "2024-03-15")  # Default date
        
        # Price Display
        self.price_var = tk.StringVar(value="Price: $0")#Variable to hold price, initially 
        ttk.Label(ticket_frame, textvariable=self.price_var).grid(row=2, column=0, columnspan=2) #Displays the dynamic price
        
        # Payment Method
        payment_frame = ttk.LabelFrame(frame, text="Payment Details", padding="10")# Labeled section for payment
        payment_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky="ew")
        
        self.payment_method = tk.StringVar() # Variable to hold selected payment method
        payment_methods = ["Credit Card", "Digital Wallet"]# List of payment method options
        ttk.Label(payment_frame, text="Payment Method:").grid(row=0, column=0)# Label for payment method
        ttk.Combobox(payment_frame, textvariable=self.payment_method, values=payment_methods).grid(row=0, column=1)# Dropdown for payment method
        
        # Buttons
        button_frame = ttk.Frame(frame)# Frame to hold action buttons
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)# Places frame below previous sections
        ttk.Button(button_frame, text="Purchase Ticket", command=self.purchase_ticket).grid(row=0, column=0, padx=5)# Button to purchase ticket
        ttk.Button(button_frame, text="View History", command=self.view_history).grid(row=0, column=1, padx=5)# Button to view order history
        ttk.Button(button_frame, text="Back to Login", command=self.back_to_login).grid(row=0, column=2, padx=5)# Button to go back to login screen

    def back_to_login(self):# Function to go back to login screen
        self.root.destroy()# Close current booking screen
        root = tk.Tk()# Create new Tkinter window
        app = LoginScreen(root, lambda user: None)# Initialize login screen
        root.mainloop()# Start the Tkinter main loop
        
        # Bind events
        self.ticket_type.trace('w', self.update_price)

    def update_price(self, *args):# Function to update the price display based on selected ticket
        prices = {
            TicketType.SINGLE_RACE.value: 100.0,
            TicketType.WEEKEND.value: 250.0,
            TicketType.SEASON.value: 1000.0,
            TicketType.GROUP.value: 80.0
        }
        selected = self.ticket_type.get()# Get selected ticket type
        if selected in prices:# If selected ticket type is valid
            self.price_var.set(f"Price: ${prices[selected]}")

    def purchase_ticket(self):# Check if all required fields are filled
        if not all([self.ticket_type.get(), self.race_date.get(), self.payment_method.get()]):
            messagebox.showerror("Error", "Please fill in all fields!")# Show error if any field is empty
            return
            
        # Validate date format
        try:
            datetime.strptime(self.race_date.get(), '%Y-%m-%d')# Validate date format (must be YYYY-MM-DD)
        except ValueError: # Show error if format is wrong
            messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD")
            return
            
        # Create a new ticket
        tickets = DataManager.load_data("tickets.pkl") if DataManager.load_data("tickets.pkl") else []
        prices = {
            TicketType.SINGLE_RACE.value: 100.0,
            TicketType.WEEKEND.value: 250.0,
            TicketType.SEASON.value: 1000.0,
            TicketType.GROUP.value: 80.0
        }
        new_ticket = Ticket(
            id=len(tickets) + 1,# Set ticket ID based on count
            type=TicketType(self.ticket_type.get()),# Set selected ticket type
            price=prices[self.ticket_type.get()],# Get the price for selected type
            event_date=self.race_date.get() #Set race date
        )
        
        # Create order and load existing orders from file, or start with an empty list
        orders = DataManager.load_data("orders.pkl") if DataManager.load_data("orders.pkl") else []
        new_order = Order(
            id=len(orders) + 1,# Set order ID based on count
            customer_id=self.user.id,# Set current user's ID
            tickets=[new_ticket],# Include the new ticket in the order
            payment_method="Credit Card"# Set payment method
        )
        
        # Save order
        orders.append(new_order)# Save updated orders to file
        DataManager.save_data(orders, "orders.pkl")
        
        messagebox.showinfo("Success", f"Ticket purchased successfully!\nTotal: ${new_order.total}")

    def view_history(self):
        orders = DataManager.load_data("orders.pkl")# Load all orders from file
        history_window = tk.Toplevel(self.root)
        history_window.title("Purchase History")# Set window title
        # Create a frame with padding
        frame = ttk.Frame(history_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S)) # Place frame in grid
        
        # Calculate and show user's loyalty points (10 points per order)
        points = len([o for o in orders if o.customer_id == self.user.id]) * 10
        ttk.Label(frame, text=f"Loyalty Points: {points}").grid(row=0, column=0, columnspan=4)
        
        # Show orders
        user_orders = [o for o in orders if o.customer_id == self.user.id]
        for i, order in enumerate(user_orders): # Loop through each of the user's orders and display them
            order_frame = ttk.Frame(frame, relief="solid", padding="10")
            order_frame.grid(row=i+1, column=0, columnspan=4, pady=5, sticky="ew")
            
            ttk.Label(order_frame, text=f"Order #{order.id}").grid(row=0, column=0)# Display order ID
            ttk.Label(order_frame, text=f"Date: {order.order_date.strftime('%Y-%m-%d')}").grid(row=0, column=1) #Display order date
            ttk.Label(order_frame, text=f"Total: ${order.total}").grid(row=1, column=0) #Display total price
            ttk.Label(order_frame, text=f"Status: {order.status}").grid(row=1, column=1) #Display order status 
            
            ttk.Button(order_frame, text="Cancel", command=lambda o=order: self.cancel_order(o, history_window)).grid(row=1, column=2)# Button to cancel the order
            if order.status == "Pending":# If the order is pending, allow modification
                ttk.Button(order_frame, text="Modify", command=lambda o=order: self.modify_order(o, history_window)).grid(row=1, column=3)
        
        ttk.Button(frame, text="Back", command=history_window.destroy).grid(row=len(user_orders)+1, column=0, columnspan=4, pady=10)

    def modify_order(self, order, parent_window):
        modify_window = tk.Toplevel(self.root)# Create a new window for modifying the selected order
        modify_window.title(f"Modify Order #{order.id}")# Set window title
        
        frame = ttk.Frame(modify_window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initialize ticket type and race date with existing order values
        self.ticket_type = tk.StringVar(value=order.tickets[0].type.value)
        self.race_date = tk.StringVar(value=order.tickets[0].event_date)
        # Label and dropdown for ticket type
        ttk.Label(frame, text="Ticket Type:").grid(row=0, column=0)
        ttk.Combobox(frame, textvariable=self.ticket_type, values=[t.value for t in TicketType]).grid(row=0, column=1)
        # Label and entry for race date
        ttk.Label(frame, text="Race Date:").grid(row=1, column=0)
        ttk.Entry(frame, textvariable=self.race_date).grid(row=1, column=1)
        # Define function to save the modified ticket
        def save_changes():
            try:
                # Define prices dictionary
                prices = {
                    TicketType.SINGLE_RACE.value: 100.0,
                    TicketType.WEEKEND.value: 250.0,
                    TicketType.SEASON.value: 1000.0,
                    TicketType.GROUP.value: 80.0
                }
                
                # Create new ticket with modified details
                new_ticket = Ticket(
                    order.tickets[0].id,
                    TicketType(self.ticket_type.get()),
                    prices[self.ticket_type.get()],
                    self.race_date.get()
                )
                
                # Update order
                orders = DataManager.load_data("orders.pkl")
                for o in orders:# Replace the ticket in the matching order
                    if o.id == order.id:
                        o._tickets = [new_ticket]# Update tickets list
                # Save the updated orders back to the file
                DataManager.save_data(orders, "orders.pkl")
                messagebox.showinfo("Success", "Order modified successfully!")# Show success message and refresh history view
                modify_window.destroy()# Close modification window
                parent_window.destroy()# Close history window
                self.view_history()# Reload updated history
                
            except ValueError as e:# Show error if something goes wrong
                messagebox.showerror("Error", str(e))
        
        ttk.Button(frame, text="Save Changes", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)# Save button to apply changes
        ttk.Button(frame, text="Cancel", command=modify_window.destroy).grid(row=3, column=0, columnspan=2)# Cancel button to close the modify window

    def cancel_order(self, order, parent_window):# Ask for confirmation before cancelling the order
        if messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this order?"):
            orders = DataManager.load_data("orders.pkl")# Load existing orders
            orders = [o for o in orders if o.id != order.id]# Remove the selected order from the list
            DataManager.save_data(orders, "orders.pkl")# Save the updated list back to the file
            messagebox.showinfo("Success", "Order cancelled successfully!")# Show confirmation message
            parent_window.destroy()# Close the history window and refresh it
            self.view_history()

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        frame = ttk.Frame(root, padding="20")# Create the main frame for the dashboard
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(frame, text="Admin Dashboard", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=4, pady=10)
        
        # Customer Management
        ttk.Button(frame, text="Manage Customers", command=self.manage_customers).grid(row=1, column=0, padx=5)
        ttk.Button(frame, text="View Sales", command=self.view_sales).grid(row=1, column=1, padx=5)
        ttk.Button(frame, text="Manage Orders", command=self.manage_orders).grid(row=1, column=2, padx=5)
        ttk.Button(frame, text="Manage Discounts", command=self.manage_discounts).grid(row=1, column=3, padx=5)
        ttk.Button(frame, text="Back to Login", command=self.back_to_login).grid(row=2, column=0, columnspan=4, pady=10)

    def manage_customers(self):# Create a new window for managing customers
        customers_window = tk.Toplevel(self.root)
        customers_window.title("Customer Management")
        frame = ttk.Frame(customers_window, padding="20")# Frame for listing customer details
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Customer list
        customers = [user for user in DataManager.load_data("users.pkl") if isinstance(user, Customer)]
        # Display customer information row by row
        for i, customer in enumerate(customers):
            ttk.Label(frame, text=f"ID: {customer.id}").grid(row=i, column=0, padx=5)
            ttk.Label(frame, text=f"Name: {customer.name}").grid(row=i, column=1, padx=5)
            ttk.Label(frame, text=f"Email: {customer.email}").grid(row=i, column=2, padx=5)
            ttk.Button(frame, text="Edit", command=lambda c=customer: self.edit_customer(c)).grid(row=i, column=3, padx=5)
            ttk.Button(frame, text="Delete", command=lambda c=customer: self.delete_customer(c, frame)).grid(row=i, column=4, padx=5)

    def edit_customer(self, customer):# Create a new window for editing the selected customer
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Customer")
        frame = ttk.Frame(edit_window, padding="20")# Frame for form inputs
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Variables to hold edited name and email
        name_var = tk.StringVar(value=customer.name)
        email_var = tk.StringVar(value=customer.email)
        # Labels and entry fields for name and email
        ttk.Label(frame, text="Name:").grid(row=0, column=0)
        ttk.Entry(frame, textvariable=name_var).grid(row=0, column=1)
        ttk.Label(frame, text="Email:").grid(row=1, column=0)
        ttk.Entry(frame, textvariable=email_var).grid(row=1, column=1)
        # Function to save the changes made
        def save_changes():
            users = DataManager.load_data("users.pkl")
            for user in users:
                if user.id == customer.id:
                    user._name = name_var.get()
                    user._email = email_var.get()
            DataManager.save_data(users, "users.pkl")# Save updated user list
            edit_window.destroy() #Close the edit window
            self.manage_customers()# Refresh customer list
        # Button to save updated information
        ttk.Button(frame, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2)

    def delete_customer(self, customer, frame):# Confirm deletion with admin
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this customer?"):
            users = DataManager.load_data("users.pkl")
            users = [user for user in users if user.id != customer.id]# Remove the selected customer by ID
            DataManager.save_data(users, "users.pkl")# Save updated user list
            self.manage_customers()# Refresh the customer list window

    def manage_orders(self):
        orders_window = tk.Toplevel(self.root)# Create a new top-level window for managing orders
        orders_window.title("Order Management")# Set the title of the orders window
        frame = ttk.Frame(orders_window, padding="20")# Create a frame inside the window with padding
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))# Place the frame in the grid layout

        orders = DataManager.load_data("orders.pkl")# Load the list of orders from the pickle file
        
        for i, order in enumerate(orders):# Loop through each order and display its details
            ttk.Label(frame, text=f"Order #{order.id}").grid(row=i, column=0, padx=5)
            ttk.Label(frame, text=f"Customer ID: {order.customer_id}").grid(row=i, column=1, padx=5)
            ttk.Label(frame, text=f"Total: ${order.total}").grid(row=i, column=2, padx=5)
            ttk.Button(frame, text="Delete", command=lambda o=order: self.delete_order(o)).grid(row=i, column=3, padx=5)

    def delete_order(self, order):# Show a confirmation dialog before deleting the order
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this order?"):
            orders = DataManager.load_data("orders.pkl")# Reload all orders from file
            orders = [o for o in orders if o.id != order.id]# Filter out the order that matches the one to delete
            DataManager.save_data(orders, "orders.pkl")# Save the updated orders list back to the file
            self.manage_orders()# Refresh the order management view to reflect changes

    def back_to_login(self):
        self.root.destroy()# Close the current window (admin dashboard)
        root = tk.Tk()# Create a new root window
        app = LoginScreen(root, lambda user: None)# Load the login screen (with a dummy callback)
        root.mainloop()# Start the main event loop for the login screen

    def view_sales(self):
        orders = DataManager.load_data("orders.pkl")# Load all orders from file
        sales_window = tk.Toplevel(self.root)# Create a new window for viewing sales
        sales_window.title("Sales Report")# Set the title of the sales report window
        
        frame = ttk.Frame(sales_window, padding="20")# Create a frame with padding inside the sales window
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))# Place the frame using grid layout
        
        
        total_sales = sum(order.total for order in orders)# Calculate total sales by summing order totals
        ttk.Label(frame, text=f"Total Sales: ${total_sales}").grid(row=0, column=0)# Show total sales amount
        
        for i, order in enumerate(orders):# Loop through and display individual order sales
            ttk.Label(frame, text=f"Order #{order.id} - ${order.total}").grid(row=i+1, column=0)# Show each order’s total

    def manage_discounts(self):
        discount_window = tk.Toplevel(self.root)# Create a new window for managing discounts
        discount_window.title("Manage Discounts")# Set the window title
        
        frame = ttk.Frame(discount_window, padding="20")# Create a frame with padding inside the discount window
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))# Place the frame using grid layout
        
        ttk.Label(frame, text="Discount %:").grid(row=0, column=0)# Add label for the discount entry
        discount_entry = ttk.Entry(frame) # Create an entry widget for user to input discount percentage
        discount_entry.grid(row=0, column=1) # Place the entry next to the label
        
        
        def apply_discount():
            try:
                discount = float(discount_entry.get()) / 100 # Convert input to decimal form (e.g., 10% → 0.1)
                orders = DataManager.load_data("orders.pkl") # Load all orders
                for order in orders:# Loop through orders
                    if order.status == "Pending":# Only apply discount to pending orders
                        order.discount = discount# Set discount attribute
                DataManager.save_data(orders, "orders.pkl") # Save updated orders
                messagebox.showinfo("Success", "Discount applied to pending orders!")# Show success message
            except ValueError:# Handle invalid input
                messagebox.showerror("Error", "Please enter a valid discount percentage")
        # Create a button to apply discount to pending orders and place it      
        ttk.Button(frame, text="Apply to Pending Orders", command=apply_discount).grid(row=1, column=0, columnspan=2) 

