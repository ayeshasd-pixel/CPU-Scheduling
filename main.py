from scheduling import run_algorithm
import tkinter as tk
from tkinter import ttk

# ================= COLORS =================

BG = "#101418"
SIDEBAR = "#151B20"
CARD = "#1B2329"
CARD_LIGHT = "#222D34"
ACCENT = "#54C2A3"
WHITE = "#F1F5F3"
MUTED = "#9AA9A5"
GREEN = "#72D6A8"
BORDER = "#2B383D"

# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("1280x800")
root.minsize(1040, 680)
root.configure(bg=BG)

# ================= SIDEBAR =================

sidebar = tk.Frame(root, bg=SIDEBAR, width=230)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

logo = tk.Label(
    sidebar,
    text="CPU  SCHEDULER",
    bg=SIDEBAR,
    fg=WHITE,
    font=("Segoe UI", 16, "bold")
)
logo.pack(pady=(35, 8))

subtitle = tk.Label(
    sidebar,
    text="PROCESS MANAGEMENT SYSTEM",
    bg=SIDEBAR,
    fg=MUTED,
    font=("Segoe UI", 8)
)
subtitle.pack(pady=(0, 40))

# Sidebar navigation buttons



def sidebar_button(text, active=False):
    btn = tk.Label(
        sidebar,
        text="   " + text,
        anchor="w",
        bg=CARD_LIGHT if active else SIDEBAR,
        fg=ACCENT if active else MUTED,
        font=("Segoe UI", 10, "bold" if active else "normal"),
        padx=15,
        pady=12,
        cursor="hand2"
    )
    btn.active = active

    btn.pack(fill="x", padx=12, pady=4)

    def on_enter(event):
        if not btn.active:
            btn.config(bg=CARD_LIGHT)

    def on_leave(event):
        if not btn.active:
            btn.config(bg=SIDEBAR)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn


dashboard_btn = sidebar_button("Dashboard", True)
process_btn = sidebar_button("Process Manager")
algorithm_btn = sidebar_button("Scheduling Algorithms")
gantt_btn = sidebar_button("Gantt Chart")
navigation_buttons = (
    dashboard_btn,
    process_btn,
    algorithm_btn,
    gantt_btn
)


def set_active_nav(selected_button):
    for button in navigation_buttons:
        button.active = button is selected_button
        button.config(
            bg=CARD_LIGHT if button.active else SIDEBAR,
            fg=ACCENT if button.active else MUTED,
            font=("Segoe UI", 10, "bold" if button.active else "normal")
        )

# Sidebar footer

footer = tk.Label(
    sidebar,
    text="CPU SCHEDULER  v1.0\nOperating Systems Project",
    bg=SIDEBAR,
    fg=MUTED,
    font=("Segoe UI", 9),
    justify="left"
)
footer.pack(side="bottom", pady=25, padx=15, anchor="w")

# ================= MAIN CONTENT =================

main = tk.Frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True, padx=38, pady=30)

# Header

header = tk.Frame(main, bg=BG)
header.pack(fill="x", pady=(0, 25))

heading = tk.Label(
    header,
    text="Dashboard",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI", 25, "bold")
)
heading.pack(side="left")

status = tk.Label(
    header,
    text="● SYSTEM READY",
    bg=BG,
    fg=GREEN,
    font=("Segoe UI", 10, "bold")
)
status.pack(side="right", pady=12)

description = tk.Label(
    main,
    text="Manage processes and visualize CPU scheduling algorithms.",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 11)
)
description.pack(anchor="w", pady=(0, 25))

# ================= STATISTICS CARDS =================

stats_frame = tk.Frame(main, bg=BG)
stats_frame.pack(fill="x", pady=(0, 25))

def create_stat_card(parent, title, value, color):
    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", padx=18, pady=(17, 8))

    tk.Label(
        card,
        text=value,
        bg=CARD,
        fg=color,
        font=("Segoe UI", 23, "bold")
    ).pack(anchor="w", padx=18, pady=(0, 17))

    return card


cards = [
    ("TOTAL PROCESSES", "0", ACCENT),
    ("AVG WAITING TIME", "0.00", GREEN),
    ("AVG TURNAROUND", "0.00", "#F59E0B"),
    ("ALGORITHMS", "6", "#B6A6E8")
]

for title, value, color in cards:
    card = create_stat_card(stats_frame, title, value, color)
    card.pack(side="left", expand=True, fill="x", padx=6)

# ================= PROCESS TABLE =================

table_card = tk.Frame(
    main,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
table_card.pack(fill="both", expand=True, pady=(0, 20))

table_header = tk.Frame(table_card, bg=CARD)
table_header.pack(fill="x", padx=20, pady=18)

tk.Label(
    table_header,
    text="Process Overview",
    bg=CARD,
    fg=WHITE,
    font=("Segoe UI", 15, "bold")
).pack(side="left")

tk.Label(
    table_header,
    text="PROCESS DETAILS",
    bg=CARD,
    fg=MUTED,
    font=("Segoe UI", 9)
).pack(side="right")

# Table styling

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    fieldbackground=CARD_LIGHT,
    background=CARD_LIGHT,
    foreground=WHITE,
    arrowcolor=WHITE,
    bordercolor=BORDER,
    lightcolor=BORDER,
    darkcolor=BORDER,
    padding=8
)

style.map(
    "TCombobox",
    fieldbackground=[("readonly", CARD_LIGHT)],
    foreground=[("readonly", WHITE)],
    selectbackground=[("readonly", ACCENT)],
    selectforeground=[("readonly", WHITE)]
)



style.configure(
    "Treeview",
    background=CARD_LIGHT,
    foreground=WHITE,
    fieldbackground=CARD_LIGHT,
    rowheight=42,
    font=("Segoe UI", 10),
    borderwidth=0
)

style.configure(
    "Treeview.Heading",
    background=SIDEBAR,
    foreground=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padding=12
)

style.map(
    "Treeview",
    background=[("selected", ACCENT)],
    foreground=[("selected", WHITE)]
)

columns = ("PID", "Arrival Time", "Burst Time", "Priority")

tree = ttk.Treeview(
    table_card,
    columns=columns,
    show="headings",
    height=7
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=130)

tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# ================= BOTTOM SECTION =================

bottom = tk.Frame(main, bg=BG)
bottom.pack(fill="x")

tk.Label(
    bottom,
    text="Select an algorithm to begin scheduling.",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 10)
).pack(side="left", pady=10)



run_button = tk.Label(
    bottom,
    text="  Run Simulation  →  ",
    bg=ACCENT,
    fg=WHITE,
    font=("Segoe UI", 11, "bold"),
    padx=20,
    pady=13,
    cursor="hand2"
)

run_button.pack(side="right")

run_button.bind(
    "<Enter>",
    lambda event: run_button.config(bg="#3BAF91")
)

run_button.bind(
    "<Leave>",
    lambda event: run_button.config(bg=ACCENT)
)


# ================= PROCESS MANAGER PAGE =================

from tkinter import messagebox

process_data = []
selected_pid = None
last_result = None
last_algorithm = None

process_page = tk.Frame(main, bg=BG)

def show_dashboard():
    process_page.place_forget()

def show_process_manager():
    process_page.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )
    process_page.lift()


dashboard_btn.bind("<Button-1>", lambda e: show_dashboard())
process_btn.bind("<Button-1>", lambda e: show_process_manager())

# ================= PAGE HEADER =================

pm_header = tk.Frame(process_page, bg=BG)
pm_header.pack(fill="x", pady=(0, 8))

tk.Label(
    pm_header,
    text="Process Manager",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI", 25, "bold")
).pack(anchor="w")

tk.Label(
    process_page,
    text="Add, update and manage processes before CPU scheduling.",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 11)
).pack(anchor="w", pady=(0, 25))

# ================= INPUT FORM =================

form_card = tk.Frame(
    process_page,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
form_card.pack(fill="x", pady=(0, 20))

tk.Label(
    form_card,
    text="Process Information",
    bg=CARD,
    fg=WHITE,
    font=("Segoe UI", 15, "bold")
).pack(anchor="w", padx=20, pady=18)

input_frame = tk.Frame(form_card, bg=CARD)
input_frame.pack(fill="x", padx=15, pady=(0, 20))

def create_input(parent, label, column):
    container = tk.Frame(parent, bg=CARD)
    container.grid(row=0, column=column, padx=8, sticky="ew")

    tk.Label(
        container,
        text=label,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(0, 8))

    entry = tk.Entry(
        container,
        bg=CARD_LIGHT,
        fg=WHITE,
        insertbackground=WHITE,
        font=("Segoe UI", 12),
        relief="flat",
        bd=0
    )
    entry.pack(fill="x", ipady=11)

    return entry

for i in range(4):
    input_frame.grid_columnconfigure(i, weight=1)

pid_entry = create_input(input_frame, "Process ID", 0)
arrival_entry = create_input(input_frame, "Arrival Time", 1)
burst_entry = create_input(input_frame, "Burst Time", 2)
priority_entry = create_input(input_frame, "Priority", 3)

# ================= PROCESS TABLE =================

manager_table_card = tk.Frame(
    process_page,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
manager_table_card.pack(fill="both", expand=True)

tk.Label(
    manager_table_card,
    text="Process List",
    bg=CARD,
    fg=WHITE,
    font=("Segoe UI", 15, "bold")
).pack(anchor="w", padx=20, pady=18)

manager_tree = ttk.Treeview(
    manager_table_card,
    columns=("PID", "Arrival", "Burst", "Priority"),
    show="headings",
    height=8
)

for col, heading in [
    ("PID", "Process ID"),
    ("Arrival", "Arrival Time"),
    ("Burst", "Burst Time"),
    ("Priority", "Priority")
]:
    manager_tree.heading(col, text=heading)
    manager_tree.column(col, anchor="center", width=130)

manager_tree.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 15)
)

# ================= INPUT FUNCTIONS =================

def clear_fields():
    global selected_pid
    selected_pid = None

    for entry in (
        pid_entry,
        arrival_entry,
        burst_entry,
        priority_entry
    ):
        entry.delete(0, tk.END)

    manager_tree.selection_remove(
        manager_tree.selection()
    )

def add_process():
    pid = pid_entry.get().strip()
    arrival = arrival_entry.get().strip()
    burst = burst_entry.get().strip()
    priority = priority_entry.get().strip()

    if not all((pid, arrival, burst, priority)):
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all four fields."
        )
        return

    if any(p["pid"] == pid for p in process_data):
        messagebox.showerror(
            "Duplicate Process",
            "This Process ID already exists."
        )
        return

    try:
        arrival = int(arrival)
        burst = int(burst)
        priority = int(priority)

        if arrival < 0 or burst <= 0 or priority <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Arrival time must be non-negative.\n"
            "Burst time and priority must be positive integers."
        )
        return

    process = {
        "pid": pid,
        "arrival": arrival,
        "burst": burst,
        "priority": priority
    }

    process_data.append(process)

    values = (pid, arrival, burst, priority)

    manager_tree.insert("", "end", iid=pid, values=values)
    tree.insert("", "end", iid=pid, values=values)

    clear_fields()

    messagebox.showinfo(
        "Success",
        f"Process {pid} added successfully!"
    )

def select_process(event):
    global selected_pid

    selection = manager_tree.selection()

    if not selection:
        return

    selected_pid = selection[0]
    values = manager_tree.item(selected_pid, "values")

    entries = (
        pid_entry,
        arrival_entry,
        burst_entry,
        priority_entry
    )

    for entry, value in zip(entries, values):
        entry.delete(0, tk.END)
        entry.insert(0, value)

def update_process():
    global selected_pid

    if selected_pid is None:
        messagebox.showwarning(
            "Select Process",
            "Please select a process to update."
        )
        return

    pid = pid_entry.get().strip()
    arrival = arrival_entry.get().strip()
    burst = burst_entry.get().strip()
    priority = priority_entry.get().strip()

    if not all((pid, arrival, burst, priority)):
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all four fields."
        )
        return

    if any(
        p["pid"] == pid and p["pid"] != selected_pid
        for p in process_data
    ):
        messagebox.showerror(
            "Duplicate Process",
            "This Process ID already exists."
        )
        return

    try:
        arrival = int(arrival)
        burst = int(burst)
        priority = int(priority)

        if arrival < 0 or burst <= 0 or priority <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter valid positive values. Arrival time can be zero."
        )
        return

    old_pid = selected_pid

    for p in process_data:
        if p["pid"] == old_pid:
            p.update({
                "pid": pid,
                "arrival": arrival,
                "burst": burst,
                "priority": priority
            })
            break

    manager_tree.delete(old_pid)
    tree.delete(old_pid)

    values = (pid, arrival, burst, priority)

    manager_tree.insert("", "end", iid=pid, values=values)
    tree.insert("", "end", iid=pid, values=values)

    clear_fields()

    messagebox.showinfo(
        "Updated",
        f"Process {pid} updated successfully!"
    )

def delete_process():
    global selected_pid

    if selected_pid is None:
        messagebox.showwarning(
            "Select Process",
            "Please select a process to delete."
        )
        return

    answer = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this process?"
    )

    if not answer:
        return

    process_data[:] = [
        p for p in process_data
        if p["pid"] != selected_pid
    ]

    manager_tree.delete(selected_pid)
    tree.delete(selected_pid)

    clear_fields()

def clear_all_processes():
    answer = messagebox.askyesno(
        "Clear All",
        "Delete all processes?"
    )

    if not answer:
        return

    process_data.clear()

    for item in manager_tree.get_children():
        manager_tree.delete(item)

    for item in tree.get_children():
        tree.delete(item)

    clear_fields()

manager_tree.bind("<<TreeviewSelect>>", select_process)

# ================= ACTION BUTTONS =================

actions = tk.Frame(form_card, bg=CARD)
actions.pack(fill="x", padx=20, pady=(0, 18))

def action_button(parent, text, color, command):
    btn = tk.Label(
        parent,
        text=text,
        bg=color,
        fg=WHITE,
        font=("Segoe UI", 10, "bold"),
        padx=17,
        pady=11,
        cursor="hand2"
    )

    btn.pack(side="left", padx=(0, 10))

    btn.bind("<Button-1>", lambda e: command())

    return btn

action_button(actions, "+ Add Process", ACCENT, add_process)
action_button(actions, "Update", "#0D9488", update_process)
action_button(actions, "Delete", "#DC2626", delete_process)
action_button(actions, "Clear All", "#475569", clear_all_processes)
action_button(actions, "Clear Fields", CARD_LIGHT, clear_fields)


# ================= SCHEDULING ALGORITHMS PAGE =================

scheduling_page = tk.Frame(main, bg=BG)

def show_scheduling_page():
    set_active_nav(algorithm_btn)
    process_page.place_forget()
    gantt_page.place_forget()

    scheduling_page.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )
    scheduling_page.lift()


def show_dashboard_all():
    set_active_nav(dashboard_btn)
    process_page.place_forget()
    scheduling_page.place_forget()
    gantt_page.place_forget()


def show_process_manager_all():
    set_active_nav(process_btn)
    scheduling_page.place_forget()
    gantt_page.place_forget()
    show_process_manager()


gantt_page = tk.Frame(main, bg=BG)

tk.Label(
    gantt_page,
    text="Gantt Chart",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI", 25, "bold")
).pack(anchor="w")

tk.Label(
    gantt_page,
    text="Follow each process across the CPU timeline.",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 11)
).pack(anchor="w", pady=(8, 24))

gantt_card = tk.Frame(
    gantt_page,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
gantt_card.pack(fill="both", expand=True)

gantt_info = tk.Label(
    gantt_card,
    text="Run a simulation to generate its timeline.",
    bg=CARD,
    fg=MUTED,
    font=("Segoe UI", 10)
)
gantt_info.pack(anchor="w", padx=20, pady=(18, 8))

gantt_canvas = tk.Canvas(
    gantt_card,
    height=300,
    bg=CARD_LIGHT,
    highlightthickness=0,
    xscrollincrement=30
)
gantt_canvas.pack(fill="both", expand=True, padx=18, pady=(0, 8))

gantt_scrollbar = ttk.Scrollbar(
    gantt_card,
    orient="horizontal",
    command=gantt_canvas.xview
)
gantt_scrollbar.pack(fill="x", padx=18, pady=(0, 16))
gantt_canvas.configure(xscrollcommand=gantt_scrollbar.set)

PROCESS_COLORS = (
    "#3B82F6",
    "#14B8A6",
    "#8B5CF6",
    "#F59E0B",
    "#EC4899",
    "#22C55E",
    "#06B6D4",
    "#F97316"
)


def render_gantt_chart():
    gantt_canvas.delete("all")

    if not last_result or not last_result.get("segments"):
        gantt_info.config(text="Run a simulation to generate its timeline.")
        gantt_scrollbar.pack_forget()
        canvas_width = max(gantt_canvas.winfo_width(), 700)
        canvas_height = max(gantt_canvas.winfo_height(), 300)
        gantt_canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))
        gantt_canvas.create_text(
            canvas_width / 2,
            canvas_height / 2,
            text="Your process timeline will appear here.",
            fill=MUTED,
            font=("Segoe UI", 12)
        )
        return

    segments = last_result["segments"]
    start_time = min(segment["start"] for segment in segments)
    end_time = max(segment["end"] for segment in segments)
    duration = max(1, end_time - start_time)
    viewport_width = max(gantt_canvas.winfo_width(), 700)
    canvas_height = max(gantt_canvas.winfo_height(), 300)
    vertical_offset = max(0, (canvas_height - 300) / 2)
    margin = 42
    pixels_per_unit = max(36, min(76, (viewport_width - margin * 2) / duration))
    plot_width = duration * pixels_per_unit
    content_width = margin * 2 + plot_width

    if content_width > viewport_width:
        if not gantt_scrollbar.winfo_manager():
            gantt_scrollbar.pack(fill="x", padx=18, pady=(0, 16))
    else:
        gantt_scrollbar.pack_forget()

    block_count = len(segments)
    block_label = "block" if block_count == 1 else "blocks"
    gantt_info.config(
        text=f"{last_algorithm}   ·   time {start_time}–{end_time}   ·   {block_count} execution {block_label}"
    )
    gantt_canvas.configure(scrollregion=(0, 0, content_width, canvas_height))

    x_start = margin
    block_top = 72 + vertical_offset
    block_bottom = 126 + vertical_offset
    axis_y = 145 + vertical_offset

    gantt_canvas.create_text(
        x_start,
        35 + vertical_offset,
        anchor="w",
        text="CPU EXECUTION",
        fill=MUTED,
        font=("Segoe UI", 9, "bold")
    )

    process_ids = list(dict.fromkeys(
        segment["pid"] for segment in segments if segment["pid"] != "IDLE"
    ))
    color_by_pid = {
        pid: PROCESS_COLORS[index % len(PROCESS_COLORS)]
        for index, pid in enumerate(process_ids)
    }

    for segment in segments:
        left = x_start + (segment["start"] - start_time) * pixels_per_unit
        right = x_start + (segment["end"] - start_time) * pixels_per_unit
        is_idle = segment["pid"] == "IDLE"
        color = "#475569" if is_idle else color_by_pid[segment["pid"]]

        gantt_canvas.create_rectangle(
            left,
            block_top,
            right,
            block_bottom,
            fill=color,
            outline=CARD_LIGHT,
            width=2
        )
        if right - left >= 32:
            gantt_canvas.create_text(
                (left + right) / 2,
                (block_top + block_bottom) / 2,
                text="IDLE" if is_idle else segment["pid"],
                fill=WHITE,
                font=("Segoe UI", 9, "bold")
            )

    tick_step = max(1, (duration + 9) // 10)
    ticks = list(range(0, duration + 1, tick_step))
    if ticks[-1] != duration:
        ticks.append(duration)

    for tick in ticks:
        x = x_start + tick * pixels_per_unit
        gantt_canvas.create_line(x, axis_y, x, axis_y + 10, fill=MUTED, width=1)
        gantt_canvas.create_text(
            x,
            axis_y + 25,
            text=str(start_time + tick),
            fill=MUTED,
            font=("Segoe UI", 9)
        )

    legend_y = 215 + vertical_offset
    legend_x = x_start
    legend_entries = [(pid, color_by_pid[pid]) for pid in process_ids]
    if any(segment["pid"] == "IDLE" for segment in segments):
        legend_entries.append(("IDLE", "#475569"))

    for label, color in legend_entries:
        gantt_canvas.create_rectangle(
            legend_x,
            legend_y - 7,
            legend_x + 14,
            legend_y + 7,
            fill=color,
            outline=""
        )
        gantt_canvas.create_text(
            legend_x + 21,
            legend_y,
            anchor="w",
            text=label,
            fill=WHITE,
            font=("Segoe UI", 9)
        )
        legend_x += 76 if label != "IDLE" else 86


def show_gantt_page():
    set_active_nav(gantt_btn)
    process_page.place_forget()
    scheduling_page.place_forget()
    gantt_page.place(relx=0, rely=0, relwidth=1, relheight=1)
    gantt_page.lift()
    root.after_idle(render_gantt_chart)


gantt_canvas.bind("<Configure>", lambda event: render_gantt_chart())


dashboard_btn.bind(
    "<Button-1>",
    lambda e: show_dashboard_all()
)

process_btn.bind(
    "<Button-1>",
    lambda e: show_process_manager_all()
)

algorithm_btn.bind(
    "<Button-1>",
    lambda e: show_scheduling_page()
)

gantt_btn.bind(
    "<Button-1>",
    lambda e: show_gantt_page()
)

# ================= PAGE HEADER =================

tk.Label(
    scheduling_page,
    text="Scheduling Algorithms",
    bg=BG,
    fg=WHITE,
    font=("Segoe UI", 25, "bold")
).pack(anchor="w", pady=(0, 8))

tk.Label(
    scheduling_page,
    text="Choose an algorithm and simulate CPU process execution.",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 11)
).pack(anchor="w", pady=(0, 25))

# ================= ALGORITHM SELECTION =================

selection_card = tk.Frame(
    scheduling_page,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
selection_card.pack(fill="x", pady=(0, 20))

tk.Label(
    selection_card,
    text="Simulation Configuration",
    bg=CARD,
    fg=WHITE,
    font=("Segoe UI", 15, "bold")
).pack(anchor="w", padx=20, pady=18)

controls = tk.Frame(selection_card, bg=CARD)
controls.pack(fill="x", padx=20, pady=(0, 20))

tk.Label(
    controls,
    text="Select Algorithm",
    bg=CARD,
    fg=MUTED,
    font=("Segoe UI", 10)
).grid(row=0, column=0, sticky="w", padx=(0, 15))

algorithm_var = tk.StringVar(value="FCFS")

algorithm_dropdown = ttk.Combobox(
    controls,
    textvariable=algorithm_var,
    values=[
        "FCFS",
        "SJF (Non-preemptive)",
        "SJF (Preemptive)",
        "Priority (Non-preemptive)",
        "Priority (Preemptive)",
        "Round Robin"
    ],
    state="readonly",
    width=27,
    font=("Segoe UI", 11)
)
algorithm_dropdown.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=(0, 20),
    ipady=7
)

tk.Label(
    controls,
    text="Time Quantum (Round Robin)",
    bg=CARD,
    fg=MUTED,
    font=("Segoe UI", 10)
).grid(row=0, column=1, sticky="w")

quantum_entry = tk.Entry(
    controls,
    bg=CARD_LIGHT,
    fg=WHITE,
    insertbackground=WHITE,
    font=("Segoe UI", 12),
    relief="flat",
    bd=0,
    width=15
)
quantum_entry.insert(0, "2")
quantum_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    ipady=11
)

controls.grid_columnconfigure(0, weight=2)
controls.grid_columnconfigure(1, weight=1)

# ================= RUN SIMULATION =================

def execute_simulation():
    global last_result, last_algorithm

    if not process_data:
        messagebox.showwarning(
            "No Processes",
            "Please add processes in Process Manager first."
        )
        return

    algorithm = algorithm_var.get()

    try:
        quantum = int(quantum_entry.get())

        if quantum <= 0:
            raise ValueError

        result = run_algorithm(
            process_data,
            algorithm,
            quantum
        )

    except ValueError as error:
        messagebox.showerror(
            "Invalid Input",
            str(error)
        )
        return

    except Exception as error:
        messagebox.showerror(
            "Simulation Error",
            str(error)
        )
        return

    last_result = result
    last_algorithm = algorithm

    # Update result table

    for item in results_tree.get_children():
        results_tree.delete(item)

    for process in result["metrics"]:
        results_tree.insert(
            "",
            "end",
            values=(
                process["pid"],
                process["completion"],
                process["turnaround"],
                process["waiting"],
                process["response"]
            )
        )

    # Update statistics

    avg_waiting_label.config(
        text=f'{result["avg_waiting"]:.2f}'
    )

    avg_turnaround_label.config(
        text=f'{result["avg_turnaround"]:.2f}'
    )

    avg_response_label.config(
        text=f'{result["avg_response"]:.2f}'
    )

    render_gantt_chart()

    messagebox.showinfo(
        "Simulation Complete",
        f"{algorithm} simulation completed successfully!"
    )


run_sim_button = tk.Label(
    selection_card,
    text="  Run Simulation  →  ",
    bg=ACCENT,
    fg=WHITE,
    font=("Segoe UI", 11, "bold"),
    padx=20,
    pady=12,
    cursor="hand2"
)
run_sim_button.pack(anchor="e", padx=20, pady=(0, 18))

run_sim_button.bind(
    "<Button-1>",
    lambda e: execute_simulation()
)

# ================= PERFORMANCE CARDS =================

metrics_frame = tk.Frame(scheduling_page, bg=BG)
metrics_frame.pack(fill="x", pady=(0, 20))

def create_metric(parent, title, value, color):
    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 9)
    ).pack(anchor="w", padx=15, pady=(14, 6))

    value_label = tk.Label(
        card,
        text=value,
        bg=CARD,
        fg=color,
        font=("Segoe UI", 20, "bold")
    )
    value_label.pack(anchor="w", padx=15, pady=(0, 14))

    return card, value_label


avg_wait_card, avg_waiting_label = create_metric(
    metrics_frame, "AVG WAITING TIME", "0.00", GREEN
)

avg_turn_card, avg_turnaround_label = create_metric(
    metrics_frame, "AVG TURNAROUND TIME", "0.00", "#F59E0B"
)

avg_response_card, avg_response_label = create_metric(
    metrics_frame, "AVG RESPONSE TIME", "0.00", "#A78BFA"
)

for card in (
    avg_wait_card,
    avg_turn_card,
    avg_response_card
):
    card.pack(side="left", expand=True, fill="x", padx=5)

# ================= RESULTS TABLE =================

results_card = tk.Frame(
    scheduling_page,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)
results_card.pack(fill="both", expand=True)

tk.Label(
    results_card,
    text="Simulation Results",
    bg=CARD,
    fg=WHITE,
    font=("Segoe UI", 15, "bold")
).pack(anchor="w", padx=20, pady=15)

results_tree = ttk.Treeview(
    results_card,
    columns=("PID", "CT", "TAT", "WT", "RT"),
    show="headings",
    height=5
)

result_columns = [
    ("PID", "Process ID"),
    ("CT", "Completion Time"),
    ("TAT", "Turnaround Time"),
    ("WT", "Waiting Time"),
    ("RT", "Response Time")
]

for col, heading in result_columns:
    results_tree.heading(col, text=heading)
    results_tree.column(
        col,
        anchor="center",
        width=110
    )

results_tree.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 15)
)

# ================= GANTT CHART LINK =================

gantt_view_link = tk.Label(
    results_card,
    text="Open graphical Gantt Chart  →",
    bg=CARD,
    fg=ACCENT,
    font=("Segoe UI", 10, "bold"),
    cursor="hand2"
)
gantt_view_link.pack(anchor="w", padx=20, pady=(5, 18))
gantt_view_link.bind("<Button-1>", lambda event: show_gantt_page())


# ================= RUN APPLICATION =================

root.mainloop()

