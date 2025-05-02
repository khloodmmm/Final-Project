import tkinter as tk
from tkinter import ttk, messagebox
from models import *

class LoginScreen:
    def __init__(self, root, on_login):
        self.root = root
        self.on_login = on_login
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Email:").grid(row=0, column=0)
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)

        tk.Button(self.frame, text="Login", command=self.login).grid(row=2, columnspan=2)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        users = load_data("users.pkl")
        for user in users:
            if user.email == email and user.authenticate(password):
                self.on_login(user)
                return
        messagebox.showerror("Error", "Invalid credentials!")

class BookingApp:
    def __init__(self, root):
        self.root = root
        self.current_user = None
        self.show_login_screen()

    def show_login_screen(self):
        LoginScreen(self.root, self.on_login_success)

    def on_login_success(self, user):
        self.current_user = user
        self.clear_screen()
        if isinstance(user, Admin):
            self.show_admin_dashboard()
        else:
            self.show_booking_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_booking_screen(self):
        tk.Label(self.root, text=f"Welcome, {self.current_user.name}!").pack()
        # Add ticket selection, cart, etc.

    def show_admin_dashboard(self):
        tk.Label(self.root, text="Admin Dashboard").pack()
        # Add sales reports, discount controls, etc.

if __name__ == "__main__":
    root = tk.Tk()
    app = BookingApp(root)
    root.mainloop()
