import tkinter as tk

import matplotlib
matplotlib.use("TkAgg") 

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from analytics import load_events, compute_funnel, stage_failures



#small UI helpers
def clear_frame(frame: tk.Frame):
    for w in frame.winfo_children():
        w.destroy()


def make_card(parent: tk.Frame, title: str, value: str) -> tk.Frame:
    card = tk.Frame(parent, bd=1, relief="solid", padx=12, pady=10)
    tk.Label(card, text=title, font=("TkDefaultFont", 11)).pack(anchor="w")
    tk.Label(card, text=value, font=("TkDefaultFont", 18, "bold")).pack(anchor="w")
    return card


def embed_bar_chart(parent: tk.Frame, title: str, labels, values, rotate=25):
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    colors = ["steelblue", "steelblue", "green", "red", "orange", "green"]
    ax.bar(labels, values, color=colors)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=rotate)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    plt.close(fig)



#dashboard refresh logic
def refresh_dashboard():
    events = load_events()
    funnel = compute_funnel(events)
    failures = stage_failures(events)

    #clear previous UI
    clear_frame(kpi_row)
    clear_frame(left_panel)
    clear_frame(right_panel)
    text.delete("1.0", tk.END)

    if not events:
        text.insert(tk.END, "No telemetry data found.\n")
        return

    #KPIs
    sessions = len({e.get("session_id") for e in events if e.get("session_id") is not None})
    stage_starts = funnel.get("Stage Starts", 0)
    stage_completes = funnel.get("Stage Completes", 0)
    stage_fails = funnel.get("Stage Fails", 0)
    completion_rate = funnel.get("Completion Rate %", 0.0)

    make_card(kpi_row, "Sessions", str(sessions)).pack(side="left", padx=8, fill="x", expand=True)
    make_card(kpi_row, "Stage Starts", str(stage_starts)).pack(side="left", padx=8, fill="x", expand=True)
    make_card(kpi_row, "Stage Fails", str(stage_fails)).pack(side="left", padx=8, fill="x", expand=True)
    make_card(kpi_row, "Completion Rate", f"{completion_rate:.1f}%").pack(side="left", padx=8, fill="x", expand=True)

    #chart 1: Funnel counts (exclude %)
    funnel_keys = ["Level Starts", "Stage Starts", "Stage Completes", "Stage Fails", "Sessions Ended", "Level Completes"]
    funnel_vals = [funnel.get(k, 0) for k in funnel_keys]
    embed_bar_chart(left_panel, "Progression Funnel (Counts)", funnel_keys, funnel_vals, rotate=30)

    #chart 2: Top failing stages
    if failures:
        items = sorted(failures.items(), key=lambda x: x[1], reverse=True)[:10]
        items = sorted(failures.items(), key=lambda x: x[1], reverse=True)
        labels = [f"L{lvl}-S{stg}" for (lvl, stg), _ in items[:10]]
        values = [v for _, v in items[:10]]
        embed_bar_chart(right_panel, "Top 10 Failing Stages", labels, values, rotate=35)
    else:
        tk.Label(right_panel, text="No stage_fail events found.", font=("TkDefaultFont", 14)).pack(padx=10, pady=10)

    #text summary (short + readable)
    text.insert(tk.END, "Summary\n")
    text.insert(tk.END, "-------\n")
    text.insert(tk.END, f"Sessions: {sessions}\n")
    text.insert(tk.END, f"Stage Starts: {stage_starts}\n")
    text.insert(tk.END, f"Stage Completes: {stage_completes}\n")
    text.insert(tk.END, f"Stage Fails: {stage_fails}\n")
    text.insert(tk.END, f"Completion Rate: {completion_rate:.1f}%\n\n")

    text.insert(tk.END, "Funnel breakdown:\n")
    for k in funnel_keys:
        text.insert(tk.END, f"  {k}: {funnel.get(k, 0)}\n")


# UI layout
root = tk.Tk()
root.title("Telemetry Analytics Dashboard")
root.geometry("1300x800")

#top bar
top = tk.Frame(root, padx=12, pady=12)
top.pack(fill="x")

tk.Label(top, text="Telemetry Analytics Dashboard", font=("TkDefaultFont", 18, "bold")).pack(side="left")
tk.Button(top, text="Refresh", width=12, command=refresh_dashboard).pack(side="right")

#KPI row
kpi_row = tk.Frame(root, padx=12, pady=6)
kpi_row.pack(fill="x")

#charts row
charts_row = tk.Frame(root, padx=12, pady=12)
charts_row.pack(fill="both", expand=True)

left_panel = tk.Frame(charts_row, bd=1, relief="solid")
left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

right_panel = tk.Frame(charts_row, bd=1, relief="solid")
right_panel.pack(side="right", fill="both", expand=True, padx=(8, 0))

#bottom text area
bottom = tk.Frame(root, padx=12, pady=0)
bottom.pack(fill="both", pady=(0, 12))

text = tk.Text(bottom, height=9, font=("TkDefaultFont", 12))
text.pack(fill="both", expand=True)

#initial render
refresh_dashboard()
root.mainloop()