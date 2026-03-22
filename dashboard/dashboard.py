import os
import sys
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from analytics import load_events, compute_funnel, stage_failures

# theme
BG_COLOR = "#171a2b"
PANEL_COLOR = "#202540"
CARD_COLOR = "#242a48"
TEXT_COLOR = "#f2f4ff"
MUTED_TEXT = "#c7cbe6"
TITLE_COLOR = "#38e1ff"

BAR_BLUE = "#5b8def"
BAR_GREEN = "#6cc36c"
BAR_ORANGE = "#f2a541"
BAR_RED = "#e76f6f"
BAR_TEAL = "#69c9c3"
BAR_GREY = "#aab2c8"

TITLE_FONT = ("Arial", 18, "bold")
BODY_FONT = ("Arial", 11)
VALUE_FONT = ("Arial", 16, "bold")


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def format_stage_label(level_id, stage_id):
    return f"Level {level_id} – Stage {stage_id}"


def make_card(parent, title, value, value_color=TEXT_COLOR):
    card = tk.Frame(parent, bg=CARD_COLOR, padx=14, pady=12)

    tk.Label(
        card,
        text=title,
        font=BODY_FONT,
        fg=MUTED_TEXT,
        bg=CARD_COLOR
    ).pack(anchor="w")

    tk.Label(
        card,
        text=value,
        font=VALUE_FONT,
        fg=value_color,
        bg=CARD_COLOR
    ).pack(anchor="w", pady=(4, 0))

    return card


def compute_stage_starts(events):
    starts = defaultdict(int)
    for e in events:
        if e.get("event_type") == "stage_start":
            key = (e.get("level_id"), e.get("stage_id"))
            starts[key] += 1
    return dict(starts)


def compute_stage_fail_rates(events):
    starts = compute_stage_starts(events)
    fails = stage_failures(events)

    fail_rates = {}
    for key, start_count in starts.items():
        fail_count = fails.get(key, 0)
        fail_rates[key] = (fail_count / start_count) * 100 if start_count else 0.0

    return fail_rates


def draw_bar_chart(parent, title, labels, values, color, value_format="count", y_label=None):
    fig, ax = plt.subplots(figsize=(4.6, 3.2))
    fig.patch.set_facecolor(PANEL_COLOR)
    ax.set_facecolor(PANEL_COLOR)

    bars = ax.bar(labels, values, color=color, edgecolor="#111522", linewidth=1.0)

    ax.set_title(title, color=TEXT_COLOR, fontsize=15, pad=10)
    if y_label:
        ax.set_ylabel(y_label, color=MUTED_TEXT, fontsize=10)

    ax.tick_params(axis="x", colors=MUTED_TEXT, rotation=20)
    ax.tick_params(axis="y", colors=MUTED_TEXT)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED_TEXT)
    ax.spines["bottom"].set_color(MUTED_TEXT)

    ax.grid(axis="y", linestyle="--", alpha=0.20, color=MUTED_TEXT)

    for bar, val in zip(bars, values):
        label = f"{val:.1f}%" if value_format == "percent" else f"{int(val)}"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            label,
            ha="center",
            va="bottom",
            fontsize=10,
            color=TEXT_COLOR,
            fontweight="bold"
        )

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    plt.close(fig)


def refresh_dashboard():
    events = load_events()
    funnel = compute_funnel(events)
    failures = stage_failures(events)
    fail_rates = compute_stage_fail_rates(events)

    clear_frame(kpi_row)
    clear_frame(left_panel)
    clear_frame(mid_panel)
    clear_frame(right_panel)
    summary_text.delete("1.0", tk.END)

    if not events:
        summary_text.insert(tk.END, "No telemetry data found.")
        return

    sessions = len({e.get("session_id") for e in events if e.get("session_id")})
    stage_starts_total = funnel.get("Stage Starts", 0)
    stage_completes_total = funnel.get("Stage Completes", 0)
    stage_fails_total = funnel.get("Stage Fails", 0)
    completion_rate = funnel.get("Completion Rate %", 0.0)

    make_card(kpi_row, "Sessions", str(sessions), BAR_BLUE).pack(side="left", padx=8, fill="x", expand=True)
    make_card(kpi_row, "Stage Starts", str(stage_starts_total), BAR_TEAL).pack(side="left", padx=8, fill="x", expand=True)
    make_card(kpi_row, "Stage Fails", str(stage_fails_total), BAR_RED).pack(side="left", padx=8, fill="x", expand=True)
    make_card(kpi_row, "Completion Rate", f"{completion_rate:.1f}%", BAR_GREEN).pack(side="left", padx=8, fill="x", expand=True)

    funnel_labels = [
        "Level Starts",
        "Stage Starts",
        "Stage Completes",
        "Stage Fails",
        "Sessions Ended",
        "Level Completes"
    ]
    funnel_values = [funnel.get(label, 0) for label in funnel_labels]

    draw_bar_chart(
        left_panel,
        "Progression Funnel (Counts)",
        funnel_labels,
        funnel_values,
        [BAR_BLUE, BAR_TEAL, BAR_GREEN, BAR_RED, BAR_GREY, BAR_ORANGE],
        value_format="count",
        y_label="Number of events"
    )

    if fail_rates:
        top_fail_rate_items = sorted(fail_rates.items(), key=lambda x: x[1], reverse=True)[:5]
        labels = [format_stage_label(level, stage) for (level, stage), _ in top_fail_rate_items]
        values = [rate for _, rate in top_fail_rate_items]

        draw_bar_chart(
            mid_panel,
            "Highest Stage Fail Rates (%)",
            labels,
            values,
            BAR_ORANGE,
            value_format="percent",
            y_label="Fail rate (%)"
        )
    else:
        tk.Label(
            mid_panel,
            text="No stage fail-rate data available.",
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            font=BODY_FONT
        ).pack(pady=30)

    if failures:
        top_fail_count_items = sorted(failures.items(), key=lambda x: x[1], reverse=True)[:5]
        labels = [format_stage_label(level, stage) for (level, stage), _ in top_fail_count_items]
        values = [count for _, count in top_fail_count_items]

        draw_bar_chart(
            right_panel,
            "Highest Stage Fail Counts",
            labels,
            values,
            BAR_RED,
            value_format="count",
            y_label="Number of fails"
        )
    else:
        tk.Label(
            right_panel,
            text="No stage failure data available.",
            bg=PANEL_COLOR,
            fg=TEXT_COLOR,
            font=BODY_FONT
        ).pack(pady=30)

    worst_fail_rate_stage = None
    worst_fail_rate = 0.0
    if fail_rates:
        worst_fail_rate_stage, worst_fail_rate = max(fail_rates.items(), key=lambda x: x[1])

    worst_fail_count_stage = None
    worst_fail_count = 0
    if failures:
        worst_fail_count_stage, worst_fail_count = max(failures.items(), key=lambda x: x[1])

    summary_lines = [
        "SUMMARY",
        "",
        f"Sessions recorded: {sessions}",
        f"Total stage starts: {stage_starts_total}",
        f"Total stage completions: {stage_completes_total}",
        f"Total stage failures: {stage_fails_total}",
        f"Overall stage completion rate: {completion_rate:.1f}%",
        ""
    ]

    if worst_fail_rate_stage is not None:
        summary_lines.append(
            f"Highest fail-rate stage: {format_stage_label(*worst_fail_rate_stage)} at {worst_fail_rate:.1f}%."
        )

    if worst_fail_count_stage is not None:
        summary_lines.append(
            f"Highest fail-count stage: {format_stage_label(*worst_fail_count_stage)} with {worst_fail_count} recorded fails."
        )

    summary_lines.append("")
    summary_lines.append(
        "Interpretation: the fail-rate chart shows which stage is hardest relative to attempts, while the fail-count chart shows where players fail most often in total."
    )

    summary_text.insert("1.0", "\n".join(summary_lines))


root = tk.Tk()
root.title("Telemetry Dashboard")
root.geometry("1450x860")
root.configure(bg=BG_COLOR)

top_bar = tk.Frame(root, bg=BG_COLOR, padx=18, pady=14)
top_bar.pack(fill="x")

tk.Label(
    top_bar,
    text="GAME TELEMETRY DASHBOARD",
    font=TITLE_FONT,
    fg=TITLE_COLOR,
    bg=BG_COLOR
).pack(side="left")

tk.Button(
    top_bar,
    text="Refresh",
    command=refresh_dashboard,
    bg="#edf2ff",
    fg="#111522",
    font=BODY_FONT,
    relief="flat",
    padx=14,
    pady=6,
    cursor="hand2"
).pack(side="right")

kpi_row = tk.Frame(root, bg=BG_COLOR, padx=18, pady=6)
kpi_row.pack(fill="x")

charts_row = tk.Frame(root, bg=BG_COLOR, padx=18, pady=12)
charts_row.pack(fill="both", expand=True)

left_panel = tk.Frame(charts_row, bg=PANEL_COLOR)
left_panel.pack(side="left", fill="both", expand=True, padx=8)

mid_panel = tk.Frame(charts_row, bg=PANEL_COLOR)
mid_panel.pack(side="left", fill="both", expand=True, padx=8)

right_panel = tk.Frame(charts_row, bg=PANEL_COLOR)
right_panel.pack(side="left", fill="both", expand=True, padx=8)

bottom_panel = tk.Frame(root, bg=BG_COLOR, padx=18, pady=0)
bottom_panel.pack(fill="both", pady=(0, 18))

summary_text = tk.Text(
    bottom_panel,
    height=10,
    bg="#0e1224",
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    font=BODY_FONT,
    relief="flat",
    wrap="word",
    padx=12,
    pady=10
)
summary_text.pack(fill="both", expand=True)

refresh_dashboard()
root.mainloop()