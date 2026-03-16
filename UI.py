import tkinter as tk
from tkinter import messagebox
from auth import check_login, get_permissions
import subprocess
import sys
import os

# store the current logged-in user
current_user = None

# get project directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def open_game():
    """Launch the main game script."""
    game_path = os.path.join(BASE_DIR, "mainGame.py")
    root.destroy()
    subprocess.Popen([sys.executable, game_path])


def open_dashboard():
    """Launch the analytics dashboard."""
    dashboard_path = os.path.join(BASE_DIR, "dashboard", "dashboard.py")
    subprocess.Popen([sys.executable, dashboard_path])


def open_balancer():
    """Placeholder for balancing toolkit."""
    messagebox.showinfo("Balancer", "Balancer screen not connected yet")


def show_role_menu(user):
    """Display menu options based on user permissions."""

    global current_user
    current_user = user

    # remove all current widgets
    for widget in root.winfo_children():
        widget.destroy()

    permissions = get_permissions(user)

    # welcome message
    tk.Label(
        root,
        text=f"Welcome, {user['username']}",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    # display role
    tk.Label(
        root,
        text=f"Role: {user['role'].title()}",
        font=("Arial", 11)
    ).pack(pady=5)

    tk.Label(
        root,
        text="Select an option:",
        font=("Arial", 12)
    ).pack(pady=10)

    # show buttons depending on permissions
    if permissions["play"]:
        tk.Button(root, text="Open Game", width=20, command=open_game).pack(pady=5)

    if permissions["dashboard"]:
        tk.Button(root, text="Open Dashboard", width=20, command=open_dashboard).pack(pady=5)

    if permissions["balance"]:
        tk.Button(root, text="Open Balancer", width=20, command=open_balancer).pack(pady=5)

    # logout returns to login screen
    tk.Button(root, text="Logout", width=20, command=show_login_page).pack(pady=15)


def login():
    """Validate credentials entered in the login form."""

    username = entry_username.get().strip()
    password = entry_password.get().strip()

    # Prevent empty login attempt
    if not username or not password:
        messagebox.showerror("Login Failed", "Please enter username and password")
        return

    user = check_login(username, password)

    if user:
        show_role_menu(user)
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")


def show_login_page():
    """Create the login interface."""

    # clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(
        root,
        text="Indie Game Telemetry Login",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    tk.Label(root, text="Username").pack(pady=5)

    global entry_username
    entry_username = tk.Entry(root, width=25)
    entry_username.pack(pady=5)

    tk.Label(root, text="Password").pack(pady=5)

    global entry_password
    entry_password = tk.Entry(root, width=25, show="*")
    entry_password.pack(pady=5)

    tk.Button(root, text="Login", width=20, command=login).pack(pady=15)


# create the main application window
root = tk.Tk()
root.title("Indie Game Telemetry System")
root.geometry("400x350")

# build the login screen
show_login_page()

# start the Tkinter event loop
root.mainloop()