
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

