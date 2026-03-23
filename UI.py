import tkinter as tk
from tkinter import messagebox
from auth import check_login, get_permissions
import subprocess
import sys
import os

current_user = None
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BG_COLOR = "#1e1e2f"
PANEL_COLOR = "#2a2a40"
TITLE_COLOR = "#00e5ff"
TEXT_COLOR = "#ffffff"
BUTTON_COLOR = "#00ffcc"
BUTTON_TEXT = "#111111"
ENTRY_BG = "#f4f4f4"

GAME_FONT = ("upheavtt", 18)
SUBTITLE_FONT = ("upheavtt", 12)
BODY_FONT = ("Arial", 11)
BUTTON_FONT = ("upheavtt", 12)


def open_game():
    """Launch the level selector / game entry screen."""
    game_path = os.path.join(BASE_DIR, "LevelSelector.py")
    subprocess.Popen([sys.executable, game_path], cwd=BASE_DIR)


def open_dashboard():
    """Launch the analytics dashboard."""
    dashboard_path = os.path.join(BASE_DIR, "dashboard", "dashboard.py")
    subprocess.Popen([sys.executable, dashboard_path], cwd=BASE_DIR)


def open_balancer():
    """Launch the balancing toolkit UI."""
    balancer_path = os.path.join(BASE_DIR, "balancing_toolkit", "balancer_ui.py")
    subprocess.Popen([sys.executable, balancer_path], cwd=BASE_DIR)


def make_game_button(parent, text, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=22,
        height=1,
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT,
        activebackground="#7fffe8",
        activeforeground="#000000",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=BUTTON_FONT
    )


def show_role_menu(user):
    """Display menu options based on user permissions."""
    global current_user
    current_user = user

    for widget in root.winfo_children():
        widget.destroy()

    permissions = get_permissions(user)

    root.configure(bg=BG_COLOR)

    container = tk.Frame(root, bg=BG_COLOR)
    container.pack(fill="both", expand=True)

    card = tk.Frame(
        container,
        bg=PANEL_COLOR,
        bd=0,
        padx=30,
        pady=25
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card,
        text=f"WELCOME, {user['username'].upper()}",
        font=GAME_FONT,
        fg=TITLE_COLOR,
        bg=PANEL_COLOR
    ).pack(pady=(0, 18))

    tk.Label(
        card,
        text=f"Role: {user['role'].title()}",
        font=SUBTITLE_FONT,
        fg=TEXT_COLOR,
        bg=PANEL_COLOR
    ).pack(pady=(0, 10))

    tk.Label(
        card,
        text="Select an option",
        font=BODY_FONT,
        fg=TEXT_COLOR,
        bg=PANEL_COLOR
    ).pack(pady=(0, 18))

    if permissions["play"]:
        make_game_button(card, "Open Game", open_game).pack(pady=6)

    if permissions["dashboard"]:
        make_game_button(card, "Open Dashboard", open_dashboard).pack(pady=6)

    if permissions["balance"]:
        make_game_button(card, "Open Balancer", open_balancer).pack(pady=6)

    tk.Button(
        card,
        text="Logout",
        width=22,
        command=show_login_page,
        bg="#ffcc66",
        fg="#111111",
        activebackground="#ffd98c",
        activeforeground="#000000",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=BUTTON_FONT
    ).pack(pady=(18, 0))


def login():
    """Validate credentials entered in the login form."""
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showerror("Login Failed", "Please enter username and password")
        return

    user = check_login(username, password)

    if user:
        show_role_menu(user)
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password")


def show_login_page():
    """Create the styled login interface."""
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=BG_COLOR)

    container = tk.Frame(root, bg=BG_COLOR)
    container.pack(fill="both", expand=True)

    card = tk.Frame(
        container,
        bg=PANEL_COLOR,
        bd=0,
        padx=35,
        pady=30
    )
    card.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        card,
        text="INDIE TELEMETRY SYSTEM",
        font=GAME_FONT,
        fg=TITLE_COLOR,
        bg=PANEL_COLOR
    ).pack(pady=(0, 8))

    tk.Label(
        card,
        text="Login to continue",
        font=BODY_FONT,
        fg=TEXT_COLOR,
        bg=PANEL_COLOR
    ).pack(pady=(0, 18))

    tk.Label(
        card,
        text="Username",
        font=SUBTITLE_FONT,
        fg=TEXT_COLOR,
        bg=PANEL_COLOR
    ).pack(anchor="w", pady=(0, 4))

    global entry_username
    entry_username = tk.Entry(
        card,
        width=26,
        font=BODY_FONT,
        bg=ENTRY_BG,
        fg="#000000",
        relief="flat",
        bd=0
    )
    entry_username.pack(pady=(0, 12), ipady=6)

    tk.Label(
        card,
        text="Password",
        font=SUBTITLE_FONT,
        fg=TEXT_COLOR,
        bg=PANEL_COLOR
    ).pack(anchor="w", pady=(0, 4))

    global entry_password
    entry_password = tk.Entry(
        card,
        width=26,
        show="*",
        font=BODY_FONT,
        bg=ENTRY_BG,
        fg="#000000",
        relief="flat",
        bd=0
    )
    entry_password.pack(pady=(0, 18), ipady=6)

    make_game_button(card, "Login", login).pack(pady=(0, 6))


root = tk.Tk()
root.title("Indie Game Telemetry System")
root.geometry("500x420")
root.configure(bg=BG_COLOR)

show_login_page()
root.mainloop()