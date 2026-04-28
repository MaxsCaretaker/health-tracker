import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import matplotlib.pyplot as plt
from datetime import date

# ── Theme Colors ────────────────────────────────────
BG = "#1e1e2e"
CARD = "#2a2a3e"
ACCENT = "#7c6af7"
TEXT = "#ffffff"
SUBTEXT = "#aaaacc"
GREEN = "#4caf50"
RED = "#ef5350"
BLUE = "#42a5f5"

CSV_FILE = "health_data.csv"

# ── Root Window ─────────────────────────────────────
root = tk.Tk()
root.title("Health Tracker")
root.geometry("700x750")
root.configure(bg=BG)
root.resizable(False, False)

# ── Style ────────────────────────────────────────────
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
    background=CARD, foreground=TEXT,
    fieldbackground=CARD, rowheight=28,
    font=("Segoe UI", 10))
style.configure("Treeview.Heading",
    background=ACCENT, foreground=TEXT,
    font=("Segoe UI", 10, "bold"))
style.map("Treeview", background=[("selected", ACCENT)])

# ── Functions ────────────────────────────────────────
def save_entry():
    entry = {
        "date": date.today().isoformat(),
        "heart_rate": heart_rate.get(),
        "blood_pressure": blood_pressure.get(),
        "weight": weight.get(),
        "sleep_hours": sleep_hours.get(),
        "mood": mood.get(),
        "energy": energy.get(),
        "exercise": exercise.get(),
    }

    if not all(entry.values()):
        messagebox.showwarning("Missing Data", "Please fill in all fields.")
        return

    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

    messagebox.showinfo("Saved", "Entry saved!")
    clear_fields()
    load_entries()

def clear_fields():
    for var in [heart_rate, blood_pressure, weight, sleep_hours, mood, energy, exercise]:
        var.set("")

def load_entries():
    for row in table.get_children():
        table.delete(row)
    if not os.path.exists(CSV_FILE):
        return
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            table.insert("", "end", values=(
                row["date"], row["heart_rate"], row["blood_pressure"],
                row["weight"], row["sleep_hours"], row["mood"],
                row["energy"], row["exercise"]
            ))

def show_chart():
    if not os.path.exists(CSV_FILE):
        messagebox.showwarning("No Data", "No entries found.")
        return

    dates, weights, moods, energies, sleeps = [], [], [], [], []
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                dates.append(row["date"])
                weights.append(float(row["weight"]))
                moods.append(float(row["mood"]))
                energies.append(float(row["energy"]))
                sleeps.append(float(row["sleep_hours"]))
            except ValueError:
                continue

    if not dates:
        messagebox.showwarning("No Data", "Not enough valid data to chart.")
        return

    plt.style.use("dark_background")
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Your Health Trends", fontsize=16, color="white")

    colors = ["#7c6af7", "#4caf50", "#42a5f5", "#ff7043"]
    datasets = [weights, moods, energies, sleeps]
    titles = ["Weight (lbs)", "Mood (1-10)", "Energy Level (1-10)", "Sleep Hours"]

    for ax, data, title, color in zip(axes.flat, datasets, titles, colors):
        ax.plot(dates, data, marker="o", color=color, linewidth=2)
        ax.set_title(title, color="white")
        ax.tick_params(axis="x", rotation=45, colors="white")
        ax.tick_params(axis="y", colors="white")
        ax.set_facecolor("#1e1e2e")
        fig.patch.set_facecolor("#1e1e2e")

    plt.tight_layout()
    plt.show()

# ── Header ───────────────────────────────────────────
header = tk.Frame(root, bg=ACCENT, pady=15)
header.pack(fill="x")
tk.Label(header, text="❤️  Health Tracker", font=("Segoe UI", 22, "bold"),
         bg=ACCENT, fg=TEXT).pack()
tk.Label(header, text="Track your vitals, sleep, mood, and activity",
         font=("Segoe UI", 10), bg=ACCENT, fg="#ddd").pack()

# ── Entry Form Card ──────────────────────────────────
card = tk.Frame(root, bg=CARD, padx=20, pady=15)
card.pack(fill="x", padx=20, pady=15)

tk.Label(card, text="New Entry", font=("Segoe UI", 13, "bold"),
         bg=CARD, fg=ACCENT).grid(row=0, column=0, columnspan=2, pady=(0,10), sticky="w")

labels = ["Heart Rate (bpm)", "Blood Pressure (e.g. 120/80)", "Weight (lbs)",
          "Sleep Hours", "Mood (1–10)", "Energy Level (1–10)", "Exercise (e.g. 30 min walk)"]

heart_rate = tk.StringVar()
blood_pressure = tk.StringVar()
weight = tk.StringVar()
sleep_hours = tk.StringVar()
mood = tk.StringVar()
energy = tk.StringVar()
exercise = tk.StringVar()
vars_list = [heart_rate, blood_pressure, weight, sleep_hours, mood, energy, exercise]

for i, (label_text, var) in enumerate(zip(labels, vars_list)):
    row = i // 2 + 1
    col = i % 2
    frame = tk.Frame(card, bg=CARD)
    frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")
    tk.Label(frame, text=label_text, font=("Segoe UI", 9),
             bg=CARD, fg=SUBTEXT).pack(anchor="w")
    tk.Entry(frame, textvariable=var, width=25,
             bg="#3a3a55", fg=TEXT, insertbackground=TEXT,
             relief="flat", font=("Segoe UI", 10)).pack(ipady=5)

# ── Buttons ──────────────────────────────────────────
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=5)

def make_btn(parent, text, cmd, color):
    return tk.Button(parent, text=text, command=cmd,
                     bg=color, fg=TEXT, font=("Segoe UI", 10, "bold"),
                     relief="flat", padx=15, pady=8, cursor="hand2")

make_btn(btn_frame, "💾  Save Entry", save_entry, GREEN).pack(side="left", padx=8)
make_btn(btn_frame, "🗑  Clear", clear_fields, RED).pack(side="left", padx=8)
make_btn(btn_frame, "📊  View Charts", show_chart, BLUE).pack(side="left", padx=8)

# ── History Table ─────────────────────────────────────
tk.Label(root, text="Past Entries", font=("Segoe UI", 13, "bold"),
         bg=BG, fg=ACCENT).pack(anchor="w", padx=20, pady=(15, 3))

cols = ("Date", "Heart Rate", "Blood Pressure", "Weight", "Sleep", "Mood", "Energy", "Exercise")
table = ttk.Treeview(root, columns=cols, show="headings", height=8)

for col in cols:
    table.heading(col, text=col)
    table.column(col, width=80, anchor="center")

table.pack(padx=20, fill="x")

load_entries()
root.mainloop()