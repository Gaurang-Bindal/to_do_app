import sqlite3
from datetime import datetime, timedelta

def connect_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            status TEXT,
            timestamp TEXT,
            reminder_time TEXT,
            priority TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_task(task, reminder_time, priority):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        'INSERT INTO task (task, status, timestamp, reminder_time, priority) VALUES (?, ?, ?, ?, ?)',
        (task, 'new', timestamp, reminder_time, priority)
    )
    conn.commit()
    conn.close()


def edit_task(task_id, new_text, new_reminder):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE task
        SET task = ?, reminder_time = ?
        WHERE id = ?
    ''', (new_text, new_reminder, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM task WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def update_task_status(task_id, new_status):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE task SET status = ? WHERE id = ?', (new_status, task_id))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM task')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def snooze_task(task_id, minutes=5):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT reminder_time FROM task WHERE id = ?', (task_id,))
    result = cursor.fetchone()
    if result and result[0]:
        try:
            old_time = datetime.strptime(result[0], "%Y-%m-%d %H:%M")
            new_time = old_time + timedelta(minutes=minutes)
            cursor.execute('UPDATE task SET reminder_time = ? WHERE id = ?', (new_time.strftime("%Y-%m-%d %H:%M"), task_id))
        except ValueError:
            pass  # Ignore if reminder_time is not in the expected format
    conn.commit()
    conn.close()