import tkinter as tk
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMS_PATH = os.path.join(BASE_DIR, "parameters.json")

class BalancerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Balancing Toolkit")
        self.root.geometry("600x500")
        self.root.configure(bg="#1e1e2f")

        self.params = self.load_params()
        self.entries = {}

        self.build_ui()

    def load_params(self):
        with open(PARAMS_PATH, "r") as f:
            return json.load(f)

    def save_params(self):
        with open(PARAMS_PATH, "w") as f:
            json.dump(self.params, f, indent=2)

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="BALANCING TOOLKIT",
            font=("upheavtt", 20),
            fg="cyan",
            bg="#1e1e2f"
        )
        title.pack(pady=10)

        self.frame = tk.Frame(self.root, bg="#1e1e2f")
        self.frame.pack(fill="both", expand=True)

        self.render_parameters()

        tk.Button(
            self.root,
            text="Apply Changes",
            command=self.apply_changes,
            bg="#00ffcc",
            fg="black",
            font=("upheavtt", 12)
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Run Suggestions",
            command=self.run_suggestions,
            bg="#ffcc00",
            fg="black",
            font=("upheavtt", 12)
        ).pack(pady=5)

        self.output = tk.Text(self.root, height=6)
        self.output.pack(fill="x", padx=10, pady=10)

    def render_parameters(self):
        row = 0
        for level, data in self.params.items():
            tk.Label(
                self.frame,
                text=level,
                fg="white",
                bg="#1e1e2f",
                font=("upheavtt", 12)
            ).grid(row=row, column=0, sticky="w", pady=5)

            row += 1

            for key, values in data.items():
                if isinstance(values, dict):
                    for stat, val in values.items():
                        label = f"{key}_{stat}"

                        tk.Label(
                            self.frame,
                            text=label,
                            fg="white",
                            bg="#1e1e2f"
                        ).grid(row=row, column=0, sticky="w")

                        entry = tk.Entry(self.frame)
                        entry.insert(0, str(val))
                        entry.grid(row=row, column=1)

                        self.entries[(level, key, stat)] = entry
                        row += 1

    def apply_changes(self):
        for (level, key, stat), entry in self.entries.items():
            try:
                self.params[level][key][stat] = float(entry.get())
            except:
                pass

        self.save_params()
        self.output.insert("end", "Changes applied successfully\n")

    def run_suggestions(self):
        self.output.insert("end", "Running rule-based suggestions...\n")

        # simple rule example
        for level in self.params:
            if self.params[level]["difficultyAttackScaling"] > 0.2:
                self.output.insert("end", f"{level}: High difficulty → suggest reducing attack scaling\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = BalancerUI(root)
    root.mainloop()