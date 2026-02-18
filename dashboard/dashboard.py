import tkinter as tk
from analytics import load_events, compute_funnel, stage_failures


def refresh_dashboard():

    events = load_events()

    text.delete("1.0", tk.END)

    if not events:
        text.insert(tk.END, "No telemetry data found.\n")
        return

    # ---------- Funnel ----------
    funnel = compute_funnel(events)

    text.insert(tk.END, "PROGRESSION FUNNEL\n")
    text.insert(tk.END, "------------------------------------\n")

    for k, v in funnel.items():
        text.insert(tk.END, f"{k}: {v}\n")

    # ---------- Failures ----------
    failures = stage_failures(events)

    text.insert(tk.END, "\nSTAGE FAILURE COUNTS\n")
    text.insert(tk.END, "-------------------------------------\n")

    if not failures:
        text.insert(tk.END, "No stage failures recorded.\n")
    else:
        for (level, stage), count in failures.items():
            text.insert(tk.END, f"[Level {level} Stage {stage}]: {count} failures\n")


# ---------- UI ----------

root = tk.Tk()
root.title("Telemetry Analytics Dashboard")
root.geometry("1020x840")

btn = tk.Button(root, text="Refresh Dashboard", command=refresh_dashboard)
btn.pack(pady=10)

text = tk.Text(root, font=("TkDefaultFont, 24"))
text.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()