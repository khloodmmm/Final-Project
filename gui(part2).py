
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

