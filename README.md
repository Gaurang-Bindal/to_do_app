# To-Do List Application with Alarm & Filtering

This is a desktop To-Do List application built with Python and Tkinter. It allows you to manage tasks, set reminders with alarms, filter tasks by status or date, and assign priorities. The app uses SQLite for persistent storage.

## Features
- Add, edit, and delete tasks
- Set reminders for tasks (with alarm sound and snooze)
- Mark tasks as done
- Filter tasks by status (new/done) and date
- Assign priority (High, Medium, Low) with color coding
- Persistent storage using SQLite
- Cross-platform alarm sound support

## Requirements
- Python 3.7+
- See `requirements.txt` for dependencies

## Installation
1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) If not on Windows, place an `alarm.mp3` file in the project directory for alarm sound.

## Usage
Run the application with:
```bash
python ui.py
```

## File Overview
- `ui.py`: Main GUI application (Tkinter)
- `database.py`: Handles SQLite database operations
- `todo.db`: SQLite database file (auto-created)

## Notes
- On Windows, the alarm uses the system beep. On other platforms, it plays `alarm.mp3` (ensure you have this file).
- The app creates `todo.db` in the working directory if it does not exist.

## Screenshots
*(Add screenshots here if desired)*

## License
MIT License (add your own license if needed) 