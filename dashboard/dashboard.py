import tkinter as tk
from analytics import load_events, compute_funnel, stage_failures


def refresh_dashboard():
    events = load_events()

    text.delete("1.0", tk.END)

    if not events:
        text.insert(tk.END, "No telemetry data found.\n")
        return

    # Funnel
    funnel = compute_funnel(events)
    text.insert(tk.END, "PROGRESSION FUNNEL\n")
    text.insert(tk.END, "------------------\n")
    for k, v in funnel.items():
        text.insert(tk.END, f"{k}: {v}\n")

    # Sticking points
    text.insert(tk.END, "\nSTAGE FAILURE COUNTS\n")
    text.insert(tk.END, "-------------------\n")
    failures = stage_failures(events)

    if not failures:
        text.insert(tk.END, "No stage failures recorded.\n")
    else:
        for stage, count in failures.items():
            text.insert(tk.END, f"Stage {stage}: {count} failures\n")


# --- UI SETUP ---
root = tk.Tk()
root.title("Telemetry Analytics Dashboard")
root.geometry("500x400")

btn = tk.Button(root, text="Refresh Dashboard", command=refresh_dashboard)
btn.pack(pady=10)

text = tk.Text(root)
text.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()