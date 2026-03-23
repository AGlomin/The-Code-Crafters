import tkinter as tk
from tkinter import ttk
import json

with open("balancing_toolkit\\parameters.json", "r") as f:
    params = json.load(f)

def save_params(self):
        with open("balancing_toolkit\\parameters.json", "w") as f:
            json.dump( params, f, indent=2)

root = tk.Tk()
root.title("Balancing Toolkit")
root.geometry("800x600")
  
levels = list(params.keys())
display_levels = [f"Level {i+1}" for i in range(len(levels))]

# mapping back for internal use
display_to_internal = dict(zip(display_levels, levels))

currentLevel = tk.StringVar()

def display_parameters():
    for panel in [ brawler_panel,  bomber_panel,  medic_panel,  en0_panel,  en1_panel,  en2_panel]:
        for widget in panel.winfo_children():
            widget.destroy()

        level_data =  params[currentLevel]
        stat_names = {
            "health": "Health",
            "attack": "Attack",
            "attack_range": "Range",
            "move_speed": "Movement"
        }

        # Players
        for char, panel in [("brawler", brawler_panel), ("bomber", bomber_panel), ("medic", medic_panel)]:
            if char in level_data:
                for stat_key, display_name in stat_names.items():
                    if stat_key in level_data[char]:
                        tk.Label(panel, text=display_name).pack()
                        entry = tk.Entry(panel, width=14)
                        entry.insert(0, str(level_data[char][stat_key]))
                        entry.pack()
                        #entries[(currentLevel, char, stat_key)] = entry

        # Enemies
        for char, panel in [("en0",  en0_panel), ("en1",  en1_panel), ("en2",  en2_panel)]:
            if char in level_data:
                for stat_key, display_name in stat_names.items():
                    if stat_key in level_data[char]:
                        tk.Label(panel, text=display_name).pack()
                        entry = tk.Entry(panel, width=14)
                        entry.insert(0, str(level_data[char][stat_key]))
                        entry.pack()
                        #entries[(currentLevel, char, stat_key)] = entry

def load_level():
    currentLevel =  level_dropdown.get()
    display_parameters()

# ---- Top bar ----
top = tk.Frame(root, padx=12, pady=12)
top.pack(fill="x")

tk.Label(top, text="Balancing Toolkit", font=("TkDefaultFont", 18, "bold")).pack(side="left")
level_dropdown = ttk.Combobox(top, textvariable=currentLevel, values=list(params.keys()), font=("TkDefaultFont", 16))
level_dropdown.pack(side="right")

# ---- Panels row ----
players_row = tk.Frame(root, padx=12, pady=12)
players_row.pack(fill="both", expand=True)

brawler_panel = tk.LabelFrame(players_row, text="Brawler", bd=1, relief="solid")
brawler_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

bomber_panel = tk.LabelFrame(players_row, text="Bomber", bd=1, relief="solid")
bomber_panel.pack(side="left", fill="both", expand=True, padx=(8, 8))

medic_panel = tk.LabelFrame(players_row, text="Medic", bd=1, relief="solid")
medic_panel.pack(side="left", fill="both", expand=True, padx=(8, 0))

# ---- Brawler ----
brawler_health_label = tk.Label(brawler_panel, text="Health")
brawler_health_label.pack()
brawler_health = tk.Entry(brawler_panel,  width=14)
brawler_health.pack()

brawler_attack_label = tk.Label(brawler_panel, text="Attack")
brawler_attack_label.pack()
brawler_attack = tk.Entry(brawler_panel,  width=14)
brawler_attack.pack()

brawler_range_label = tk.Label(brawler_panel, text="Range")
brawler_range_label.pack()
brawler_range = tk.Entry(brawler_panel,  width=14)
brawler_range.pack()

brawler_movement_label = tk.Label(brawler_panel, text="Movement")
brawler_movement_label.pack()
brawler_movement = tk.Entry(brawler_panel,  width=14)
brawler_movement.pack()

# ---- Bomber ----
bomber_health_label = tk.Label(bomber_panel, text="Health")
bomber_health_label.pack()
bomber_health = tk.Entry(bomber_panel,  width=14)
bomber_health.pack()

bomber_attack_label = tk.Label(bomber_panel, text="Attack")
bomber_attack_label.pack()
bomber_attack = tk.Entry(bomber_panel,  width=14)
bomber_attack.pack()

bomber_range_label = tk.Label(bomber_panel, text="Range")
bomber_range_label.pack()
bomber_range = tk.Entry(bomber_panel,  width=14)
bomber_range.pack()

bomber_movement_label = tk.Label(bomber_panel, text="Movement")
bomber_movement_label.pack()
bomber_movement = tk.Entry(bomber_panel,  width=14)
bomber_movement.pack()

# ---- Medic ----

medic_health_label = tk.Label(medic_panel, text="Health")
medic_health_label.pack()
medic_health = tk.Entry(medic_panel,  width=14)
medic_health.pack()

medic_attack_label = tk.Label(medic_panel, text="Attack")
medic_attack_label.pack()
medic_attack = tk.Entry(medic_panel,  width=14)
medic_attack.pack()

medic_range_label = tk.Label(medic_panel, text="Range")
medic_range_label.pack()
medic_range = tk.Entry(medic_panel,  width=14)
medic_range.pack()

medic_movement_label = tk.Label(medic_panel, text="Movement")
medic_movement_label.pack()
medic_movement = tk.Entry(medic_panel,  width=14)
medic_movement.pack()

# ---- Enemies row ----
enemies_row = tk.Frame(root, padx=12, pady=12)
enemies_row.pack(fill="both", expand=True)

en0_panel = tk.LabelFrame(enemies_row, text="en0", bd=1, relief="solid")
en0_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

en1_panel = tk.LabelFrame(enemies_row, text="en1", bd=1, relief="solid")
en1_panel.pack(side="left", fill="both", expand=True, padx=(8, 8))

en2_panel = tk.LabelFrame(enemies_row, text="en2", bd=1, relief="solid")
en2_panel.pack(side="left", fill="both", expand=True, padx=(8, 0))


# ---- en0 ----
en0_health_label = tk.Label(en0_panel, text="Health")
en0_health_label.pack()
en0_health = tk.Entry(en0_panel,  width=14)
en0_health.pack()

en0_attack_label = tk.Label(en0_panel, text="Attack")
en0_attack_label.pack()
en0_attack = tk.Entry(en0_panel,  width=14)
en0_attack.pack()

en0_range_label = tk.Label(en0_panel, text="Range")
en0_range_label.pack()
en0_range = tk.Entry(en0_panel,  width=14)
en0_range.pack()

en0_movement_label = tk.Label(en0_panel, text="Movement")
en0_movement_label.pack()
en0_movement = tk.Entry(en0_panel,  width=14)
en0_movement.pack()

# ---- en1 ----
en1_health_label = tk.Label(en1_panel, text="Health")
en1_health_label.pack()
en1_health = tk.Entry(en1_panel,  width=14)
en1_health.pack()

en1_attack_label = tk.Label(en1_panel, text="Attack")
en1_attack_label.pack()
en1_attack = tk.Entry(en1_panel,  width=14)
en1_attack.pack()

en1_range_label = tk.Label(en1_panel, text="Range")
en1_range_label.pack()
en1_range = tk.Entry(en1_panel,  width=14)
en1_range.pack()

en1_movement_label = tk.Label(en1_panel, text="Movement")
en1_movement_label.pack()
en1_movement = tk.Entry(en1_panel,  width=14)
en1_movement.pack()

# ---- en2 ----

en2_health_label = tk.Label(en2_panel, text="Health")
en2_health_label.pack()
en2_health = tk.Entry(en2_panel,  width=14)
en2_health.pack()

en2_attack_label = tk.Label(en2_panel, text="Attack")
en2_attack_label.pack()
en2_attack = tk.Entry(en2_panel,  width=14)
en2_attack.pack()

en2_range_label = tk.Label(en2_panel, text="Range")
en2_range_label.pack()
en2_range = tk.Entry(en2_panel,  width=14)
en2_range.pack()

en2_movement_label = tk.Label(en2_panel, text="Movement")
en2_movement_label.pack()
en2_movement = tk.Entry(en2_panel,  width=14)
en2_movement.pack()


levelList = ttk.Combobox(top, textvariable=currentLevel, values=display_levels, font = ("TkDefaultFont", 20))
levelList.bind("<<ComboboxSelected>>", load_level)
currentLevel.set(levels[0])

#refresh_dashboard()
root.mainloop()