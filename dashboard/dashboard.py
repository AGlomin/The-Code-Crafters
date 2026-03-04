import tkinter as tk

import matplotlib
matplotlib.use("TkAgg") 

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from analytics import load_events, compute_funnel, stage_failures

from collections import defaultdict

def compute_stage_dropoff(events):
    starts = defaultdict(int)
    fails = defaultdict(int)

    for e in events:
        et = e.get("event_type")
        key = (e.get("level_id"), e.get("stage_id"))

        if et == "stage_start":
            starts[key] += 1
        elif et == "stage_fail":
            fails[key] += 1

    drop = {}
    for key, s in starts.items():
        f = fails.get(key, 0)
        drop[key] = (f / s) * 100 if s else 0.0

    return drop



#small UI helpers
def clear_frame(frame: tk.Frame):
    for w in frame.winfo_children():
        w.destroy()


def make_card(parent: tk.Frame, title: str, value: str) -> tk.Frame:
    card = tk.Frame(parent, bd=1, relief="solid", padx=12, pady=10)
    tk.Label(card, text=title, font=("TkDefaultFont", 11)).pack(anchor="w")
    tk.Label(card, text=value, font=("TkDefaultFont", 18, "bold")).pack(anchor="w")
    return card


def embed_bar_chart(parent: tk.Frame, title: str, labels, values, rotate=25, show_labels=True, percent_only=False):
    fig, ax = plt.subplots(figsize=(4, 3))
    colors = ["steelblue", "steelblue", "green", "red", "orange", "green"]
    ax.bar(labels, values, color=colors)
    # add value + percentage labels above bars
    if show_labels:
        max_val = max(values) if values else 1

        for i, v in enumerate(values):
            pct = (v / max_val) * 100 if max_val else 0

            if percent_only:
                label = f"{v:.1f}%"
            else:
                label = f"{v}\n({pct:.0f}%)"

            ax.text(
                i,
                v * 0.5,
                label,
                ha="center",
                va="center",
                color="black",
                fontsize=9,
                fontweight="bold"
            )
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
    dropoff = compute_stage_dropoff(events)

    #clear previous UI
    clear_frame(kpi_row)
    clear_frame(left_panel)
    clear_frame(mid_panel)
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
    embed_bar_chart(left_panel, "Progression Funnel (Counts)", funnel_keys, funnel_vals, rotate=35)

    #chart 2: Drop-off rate (%), top 10 worst stages
    if dropoff:
        items = sorted(dropoff.items(), key=lambda x: x[1], reverse=True)[:10]
        labels = [f"L{lvl}-S{stg}" for (lvl, stg), _ in items]
        values = [round(v, 1) for _, v in items]
        embed_bar_chart(mid_panel, "Top 10 Drop-off Stages (%)", labels, values, rotate=35, percent_only=True)
    else:
        tk.Label(mid_panel, text="No stage_start events found.", font=("TkDefaultFont", 14)).pack(padx=10, pady=10)

    #chart 3: Top failing stages
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

    worst = max(dropoff.values()) if dropoff else 0.0
    text.insert(tk.END, f"Highest Drop-off Stage (%): {worst:.1f}%\n")

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
#charts row
charts_row = tk.Frame(root, padx=12, pady=12)
charts_row.pack(fill="both", expand=True)

left_panel = tk.Frame(charts_row, bd=1, relief="solid")
left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

mid_panel = tk.Frame(charts_row, bd=1, relief="solid")
mid_panel.pack(side="left", fill="both", expand=True, padx=(8, 8))

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