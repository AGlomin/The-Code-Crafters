# comment to try recommit file as others didnt get it?
 
import tkinter as tk
from tkinter import ttk
import json
import os

import rule_based_suggestions as rbs


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMS_PATH = os.path.join(BASE_DIR, "parameters.json")

TITLE_FONT = ("Arial", 20, "bold")
BODY_FONT = ("Arial", 18)
VALUE_FONT = ("Arial", 15, "bold")

class BalancerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Balancing Toolkit")
        self.root.geometry("1200x1000")

        self.params = self.load_params()
        self.entries = {}
        self.current_level = list(self.params.keys())[0]

        self.build_ui()

    def load_params(self):
        with open(PARAMS_PATH, "r") as f:
            return json.load(f)

    def save_params(self):
        with open(PARAMS_PATH, "w") as f:
            json.dump(self.params, f, indent=2)

    def build_ui(self):
        # ---- Top bar ----
        self.top = tk.Frame(self.root, padx=12, pady=12, bg="#1e1e2f")
        self.top.pack(fill="x")

        tk.Label(self.top, text="Balancing Toolkit", font=TITLE_FONT, fg="cyan", bg="#1e1e2f").pack(side="left")
        
        # Difficulty scaling entry
        self.difficulty_frame = tk.Frame(self.top, bg="#1e1e2f")
        self.difficulty_frame.pack(side="right", padx=(10, 0))
        tk.Label(self.difficulty_frame, text="Difficulty Scaling:", fg="white", bg="#1e1e2f", font=BODY_FONT).pack(side="left")
        self.difficulty_entry = tk.Entry(self.difficulty_frame, width=8, font=BODY_FONT)
        self.difficulty_entry.pack(side="left")
        
        self.level_dropdown = ttk.Combobox(self.top, values=list(self.params.keys()), font=BODY_FONT)
        self.level_dropdown.pack(side="right")
        self.level_dropdown.bind("<<ComboboxSelected>>", self.load_level)
        self.level_dropdown.set(self.current_level)

        # ---- Players row ----
        self.players_row = tk.Frame(self.root, padx=12, pady=12)
        self.players_row.pack(fill="both", expand=True)

        self.brawler_panel = tk.LabelFrame(self.players_row, text="Brawler", bd=1, relief="solid", font=BODY_FONT)
        self.brawler_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.bomber_panel = tk.LabelFrame(self.players_row, text="Bomber", bd=1, relief="solid", font=BODY_FONT)
        self.bomber_panel.pack(side="left", fill="both", expand=True, padx=(8, 8))

        self.medic_panel = tk.LabelFrame(self.players_row, text="Medic", bd=1, relief="solid", font=BODY_FONT)
        self.medic_panel.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # ---- Enemies row ----
        self.enemies_row = tk.Frame(self.root, padx=12, pady=12)
        self.enemies_row.pack(fill="both", expand=True)

        self.en0_panel = tk.LabelFrame(self.enemies_row, text="en0", bd=1, relief="solid", font=BODY_FONT)
        self.en0_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.en1_panel = tk.LabelFrame(self.enemies_row, text="en1", bd=1, relief="solid", font=BODY_FONT)
        self.en1_panel.pack(side="left", fill="both", expand=True, padx=(8, 8))

        self.en2_panel = tk.LabelFrame(self.enemies_row, text="en2", bd=1, relief="solid", font=BODY_FONT)
        self.en2_panel.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # Render parameters for current selected level
        self.render_parameters()

        # Buttons
        tk.Button(
            self.root,
            text="Apply Changes",
            command=self.apply_changes,
            bg="#00ffcc",
            fg="black",
            font=BODY_FONT
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Run Suggestions",
            command=self.run_suggestions,
            bg="#ffcc00",
            fg="black",
            font=BODY_FONT
        ).pack(pady=5)

        self.output = tk.Text(self.root, height=6)
        self.output.pack(fill="x", padx=10, pady=10)

    def render_parameters(self):
        # Clear existing entries
        for panel in [self.brawler_panel, self.bomber_panel, self.medic_panel, self.en0_panel, self.en1_panel, self.en2_panel]:
            for widget in panel.winfo_children():
                widget.destroy()

        #linking backend names to display names
        level_data = self.params[self.current_level]
        
        # Set difficulty scaling value
        self.difficulty_entry.delete(0, tk.END)
        self.difficulty_entry.insert(0, str(level_data.get("difficultyAttackScaling", 0)))
        
        stat_names = {
            "health": "Health",
            "attack": "Attack",
            "attack_range": "Range",
            "move_speed": "Movement"
        }

        # Players
        for char, panel in [("brawler", self.brawler_panel), ("bomber", self.bomber_panel), ("medic", self.medic_panel)]:
            if char in level_data:
                for stat_key, display_name in stat_names.items():
                    if stat_key in level_data[char]:
                        tk.Label(panel, text=display_name, font=BODY_FONT).pack()
                        entry = tk.Entry(panel, width=14, font=VALUE_FONT)
                        entry.insert(0, str(level_data[char][stat_key]))
                        entry.pack()
                        self.entries[(self.current_level, char, stat_key)] = entry

        # Enemies
        for char, panel in [("en0", self.en0_panel), ("en1", self.en1_panel), ("en2", self.en2_panel)]:
            if char in level_data:
                for stat_key, display_name in stat_names.items():
                    if stat_key in level_data[char]:
                        tk.Label(panel, text=display_name, font=BODY_FONT).pack()
                        entry = tk.Entry(panel, width=14, font=VALUE_FONT)
                        entry.insert(0, str(level_data[char][stat_key]))
                        entry.pack()
                        self.entries[(self.current_level, char, stat_key)] = entry

    def load_level(self, event):
        self.current_level = self.level_dropdown.get()
        self.render_parameters()

    def apply_changes(self):
        for (level, char, stat), entry in self.entries.items():
            if level == self.current_level:
                try:
                    self.params[level][char][stat] = float(entry.get())
                except ValueError:
                    pass
        
        # Handle difficulty scaling
        try:
            self.params[self.current_level]["difficultyAttackScaling"] = float(self.difficulty_entry.get())
        except ValueError:
            pass
        
        self.save_params()
        self.output.insert("end", "Changes applied successfully\n")

    def run_suggestions(self):
        self.output.insert("end", "Running rule-based suggestions...\n")
        # Simple rule example - need to change to the rules malika made
        suggestions = rbs.suggest_level_changes(self.params, self.current_level)
        for suggestion in suggestions:
            self.output.insert("end", f"{self.current_level}: {suggestion}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = BalancerUI(root)
    root.mainloop()