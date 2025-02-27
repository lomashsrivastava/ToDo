import tkinter as tk
from tkinter import ttk, messagebox
import json
import pandas as pd
from datetime import datetime
from tkinter.font import Font

# File paths for saving data
JSON_FILE = "todo_data.json"
EXCEL_FILE = "todo_data.xlsx"

# Load existing tasks from JSON
def load_tasks():
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to JSON
def save_tasks_to_json():
    with open(JSON_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Save tasks to Excel
def save_tasks_to_excel():
    df = pd.DataFrame(tasks)
    df.to_excel(EXCEL_FILE, index=False)
    messagebox.showinfo("Success", f"Tasks saved to {EXCEL_FILE}")

# Add a new task
def add_task():
    title = entry_title.get()
    description = entry_description.get("1.0", tk.END).strip()
    priority = combo_priority.get()

    if not title:
        messagebox.showwarning("Input Error", "Title is required!")
        return

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "priority": priority,
        "completed": False,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    save_tasks_to_json()
    update_task_list()
    clear_inputs()
    messagebox.showinfo("Success", "Task added successfully!")

# Mark a task as completed
def mark_completed():
    selected_task = task_list.selection()
    if not selected_task:
        messagebox.showwarning("Selection Error", "Please select a task!")
        return

    task_id = int(task_list.item(selected_task, "values")[0])
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break
    save_tasks_to_json()
    update_task_list()

# Delete a task
def delete_task():
    selected_task = task_list.selection()
    if not selected_task:
        messagebox.showwarning("Selection Error", "Please select a task!")
        return

    task_id = int(task_list.item(selected_task, "values")[0])
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            break
    save_tasks_to_json()
    update_task_list()

# Filter tasks by status
def filter_tasks():
    status = filter_var.get()
    if status == "All":
        update_task_list()
    elif status == "Completed":
        filtered_tasks = [task for task in tasks if task["completed"]]
        update_task_list(filtered_tasks)
    elif status == "Pending":
        filtered_tasks = [task for task in tasks if not task["completed"]]
        update_task_list(filtered_tasks)

# Update the task list display
def update_task_list(task_list_data=None):
    task_list.delete(*task_list.get_children())
    data = task_list_data if task_list_data else tasks
    for task in data:
        status = "✔️" if task["completed"] else "❌"
        task_list.insert("", "end", values=(
            task["id"], task["title"], task["description"], task["priority"], status
        ))

# Clear input fields
def clear_inputs():
    entry_title.delete(0, tk.END)
    entry_description.delete("1.0", tk.END)
    combo_priority.set("Low")

# Load tasks on startup
tasks = load_tasks()

# UI Setup
app = tk.Tk()
app.title("Advanced To-Do Application")
app.geometry("1000x700")
app.configure(bg="#2c3e50")

# Custom Fonts
title_font = Font(family="Poppins", size=16, weight="bold")
label_font = Font(family="Roboto", size=12)
button_font = Font(family="Roboto", size=12, weight="bold")

# Gradient Background
gradient_frame = tk.Frame(app, bg="#2c3e50")
gradient_frame.pack(fill=tk.BOTH, expand=True)

# Left Frame for Input
left_frame = ttk.Frame(gradient_frame, padding="20")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Application Title
label_title = ttk.Label(left_frame, text="To-Do Application", font=title_font, foreground="#ecf0f1", background="#2c3e50")
label_title.pack(pady=10)

# Task Title
label_title = ttk.Label(left_frame, text="Title:", font=label_font, foreground="#ecf0f1", background="#2c3e50")
label_title.pack(pady=5)
entry_title = ttk.Entry(left_frame, font=label_font)
entry_title.pack(pady=5, fill=tk.X)

# Task Description
label_description = ttk.Label(left_frame, text="Description:", font=label_font, foreground="#ecf0f1", background="#2c3e50")
label_description.pack(pady=5)
entry_description = tk.Text(left_frame, height=5, font=label_font)
entry_description.pack(pady=5, fill=tk.X)

# Task Priority
label_priority = ttk.Label(left_frame, text="Priority:", font=label_font, foreground="#ecf0f1", background="#2c3e50")
label_priority.pack(pady=5)
combo_priority = ttk.Combobox(left_frame, values=["Low", "Medium", "High"], font=label_font)
combo_priority.set("Low")
combo_priority.pack(pady=5, fill=tk.X)

# Add Task Button
button_add = ttk.Button(left_frame, text="➕ Add Task", command=add_task, style="Accent.TButton")
button_add.pack(pady=10, fill=tk.X)

# Right Frame for Task List
right_frame = ttk.Frame(gradient_frame, padding="20")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Task List
task_list = ttk.Treeview(right_frame, columns=("ID", "Title", "Description", "Priority", "Status"), show="headings")
task_list.heading("ID", text="ID")
task_list.heading("Title", text="Title")
task_list.heading("Description", text="Description")
task_list.heading("Priority", text="Priority")
task_list.heading("Status", text="Status")
task_list.column("ID", width=50)
task_list.column("Title", width=150)
task_list.column("Description", width=300)
task_list.column("Priority", width=100)
task_list.column("Status", width=100)
task_list.pack(fill=tk.BOTH, expand=True)

# Filter Options
filter_var = tk.StringVar(value="All")
filter_frame = ttk.Frame(right_frame)
filter_frame.pack(pady=10)
ttk.Radiobutton(filter_frame, text="All", variable=filter_var, value="All", command=filter_tasks).pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(filter_frame, text="Completed", variable=filter_var, value="Completed", command=filter_tasks).pack(side=tk.LEFT, padx=5)
ttk.Radiobutton(filter_frame, text="Pending", variable=filter_var, value="Pending", command=filter_tasks).pack(side=tk.LEFT, padx=5)

# Action Buttons
button_frame = ttk.Frame(right_frame)
button_frame.pack(pady=10)
ttk.Button(button_frame, text="✔️ Mark Completed", command=mark_completed).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="🗑️ Delete Task", command=delete_task).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="💾 Save to Excel", command=save_tasks_to_excel).pack(side=tk.LEFT, padx=5)

# Load tasks on startup
update_task_list()

# Run the application
app.mainloop()