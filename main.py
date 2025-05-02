from gui import BookingApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grand Prix Booking System")
    app = BookingApp(root)
    root.mainloop()
