
# Import the tkinter module for creating the GUI
import tkinter as tk

# Import GUI screen classes and model classes from separate modules
from A3.gui import LoginScreen, TicketBookingScreen, AdminDashboard
from models import Admin, DataManager

# Define the main application class for the Grand Prix ticket booking system
class GrandPrixApp:
    # Constructor initializes the application
    def __init__(self, root):
        self.root = root  # Store the root window
        self.root.title("Grand Prix Experience")  # Set the window title
        self.current_user = None  # Initialize the currently logged-in user as None
        self.setup_admin()  # Ensure an admin user exists
        self.show_login()  # Show the login screen

    # Method to create a default admin account if one doesn't already exist
    def setup_admin(self):
        users = DataManager.load_data("users.pkl")  # Load existing users from a file
        # Check if any user is an instance of the Admin class
        if not any(isinstance(user, Admin) for user in users):
            # If no admin found, create a default admin account
            admin = Admin(0, "Admin", "admin@grandprix.com", "admin123")
            users.append(admin)  # Add the admin to the list of users
            DataManager.save_data(users, "users.pkl")  # Save the updated users list

    # Method to display the login screen
    def show_login(self):
        self.clear_window()  # Clear any existing GUI elements
        LoginScreen(self.root, self.on_login_success)  # Display the login screen and pass callback function

    # Callback method called when login is successful
    def on_login_success(self, user):
        self.current_user = user  # Store the logged-in user
        self.clear_window()  # Clear the screen
        if isinstance(user, Admin):
            AdminDashboard(self.root)  # Show admin dashboard if user is an admin
        else:
            TicketBookingScreen(self.root, user)  # Show ticket booking screen for regular users

    # Helper method to clear all widgets from the window
    def clear_window(self):
        for widget in self.root.winfo_children():  # Iterate through all child widgets
            widget.destroy()  # Remove each widget from the window

# If this file is run directly, create the root window and start the app
if __name__ == "__main__":
    root = tk.Tk()  # Create the main tkinter window
    app = GrandPrixApp(root)  # Instantiate the application
    root.mainloop()  # Start the tkinter event loop
