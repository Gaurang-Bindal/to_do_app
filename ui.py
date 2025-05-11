import tkinter as tk
from tkinter import messagebox
import database
from datetime import datetime
import threading
import time
import platform
from tkcalendar import DateEntry


# For sound alarm
try:
    if platform.system() == "Windows":
        import winsound
    else:
        from playsound import playsound
except ImportError:
    print("Sound module missing. Install playsound if not on Windows.")

database.connect_db()

root = tk.Tk()
root.title("To-Do List with Alarm & Filtering")
root.geometry("700x650")

task_list = tk.Listbox(root, width=100, height=20)
task_list.pack(pady=10)

task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)
task_entry.insert(0, "Enter Task")

reminder_date = DateEntry(root, width=17, date_pattern="yyyy-mm-dd")
reminder_date.pack(pady=5)


priority_var = tk.StringVar(value="Medium")
priority_menu = tk.OptionMenu(root, priority_var, "High", "Medium", "Low")
priority_menu.pack(pady=5)

filter_status = tk.Entry(root, width=30)
filter_status.pack(pady=5)
filter_status.insert(0, "Filter by status (new/done)")

filter_date = tk.Entry(root, width=30)
filter_date.pack(pady=5)
filter_date.insert(0, "Filter by date (YYYY-MM-DD)")

check_vars = {}

def load_task(filter_by_status=None, filter_by_date=None):
    task_list.delete(0, tk.END)
    check_vars.clear()
    tasks = database.get_tasks()
    for task in tasks:
        task_id, task_text, status, timestamp, alarm, priority = task
        if filter_by_status and status != filter_by_status:
            continue
        if filter_by_date and not timestamp.startswith(filter_by_date):
            continue
        display = f"ID:{task_id} | {task_text} | Status: {status} | Time: {timestamp} | Alarm: {alarm} | Priority: {priority}"
        task_list.insert(tk.END, display)

        # Color coding
        index = task_list.size() - 1
        if priority == "High":
            task_list.itemconfig(index, {'fg': 'red'})
        elif priority == "Medium":
            task_list.itemconfig(index, {'fg': 'orange'})
        elif priority == "Low":
            task_list.itemconfig(index, {'fg': 'green'})


def extract_id_from_selection():
    try:
        selected = task_list.get(task_list.curselection())
        return int(selected.split("|")[0].split(":")[1].strip())
    except:
        return None

def add_new_task():
    task = task_entry.get()
    reminder_date_val = reminder_date.get()
    priority = priority_var.get()
    if task and reminder_date_val:
        try:
            datetime.strptime(reminder_date_val, "%Y-%m-%d")  # validate format
            database.add_task(task, reminder_date_val, priority)
            load_task()
            task_entry.delete(0, tk.END)
            priority_var.set("Medium")
        except ValueError:
            messagebox.showwarning("Invalid Format", "Reminder must be in YYYY-MM-DD format")
    else:
        messagebox.showwarning("Warning", "Please enter a task and reminder time.")

def delete_selected_task():
    task_id = extract_id_from_selection()
    if task_id is not None:
        database.delete_task(task_id)
        load_task()
    else:
        messagebox.showwarning("Warning", "Please select a task to delete.")

def update_selected_task_status():
    task_id = extract_id_from_selection()
    if task_id is not None:
        database.update_task_status(task_id, "done")
        load_task()
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as done.")

def filter_tasks():
    status = filter_status.get().strip()
    date = filter_date.get().strip()
    status = status if status else None
    date = date if date else None
    load_task(filter_by_status=status, filter_by_date=date)

def edit_selected_task():
    task_id = extract_id_from_selection()
    new_text = task_entry.get()
    new_reminder = reminder_date.get()
    if task_id and new_text and new_reminder:
        try:
            datetime.strptime(new_reminder, "%Y-%m-%d")  # validate format
            database.edit_task(task_id, new_text, new_reminder)
            load_task()
            task_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Invalid Format", "Reminder must be in YYYY-MM-DD format")
    else:
        messagebox.showwarning("Warning", "Select a task and fill both fields to edit.")

def play_alarm_sound():
    try:
        if platform.system() == "Windows":
            winsound.Beep(1000, 1000)
        else:
            playsound('alarm.mp3')  # You can replace this with any .mp3 path
    except:
        print("Unable to play sound.")

def check_reminders():
    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        tasks = database.get_tasks()
        for task in tasks:
            if len(task) == 6:
                task_id, task_text, status, _, reminder_time, _ = task
            else:
                continue
            if reminder_time and reminder_time == now and status != 'done':
                def show_reminder_popup():
                    response = messagebox.askquestion("Task Reminder", f"Reminder for task:\n{task_text}\n\nSnooze for 5 minutes?", icon='question')
                    if response == 'yes':
                        database.snooze_task(task_id, minutes=5)
                        load_task()
                    else:
                        messagebox.showinfo("Reminder", f"Task: {task_text}")
                        play_alarm_sound()

                # Run the popup in the main thread
                root.after(0, show_reminder_popup)
        time.sleep(30)


# Buttons
add_button = tk.Button(root, text="Add Task", command=add_new_task)
add_button.pack()

delete_button = tk.Button(root, text="Delete Task", command=delete_selected_task)
delete_button.pack()

done_button = tk.Button(root, text="Mark Task as Done", command=update_selected_task_status)
done_button.pack()

edit_button = tk.Button(root, text="Edit Task", command=edit_selected_task)
edit_button.pack()

filter_button = tk.Button(root, text="Apply Filter", command=filter_tasks)
filter_button.pack()

load_task()

# Start alarm check in background
threading.Thread(target=check_reminders, daemon=True).start()

root.mainloop()