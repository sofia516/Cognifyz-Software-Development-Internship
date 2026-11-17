# Level 3, Task 5: Task Manager with File I/O

A console task manager based on Level 2, Task 3. It supports creating, displaying, updating, and deleting tasks. Each task has an ID, a required title, a description, and a `Pending` or `Completed` status.

## Run the application

```bash
python main.py
```

Use the numbered menu to manage tasks. Leave update fields blank to keep their current values.

## Storage

Tasks are stored as readable JSON text in `tasks.txt` beside `main.py`. The application loads this file when it starts and saves after each create, update, or delete operation. If the file does not exist, the application starts with an empty list and creates the file. Invalid records are skipped; unreadable or malformed files produce a warning and the application remains usable. File access errors are reported without stopping the menu.

## Run the tests

```bash
python -m unittest -v
```

Tests use temporary directories and files, so they do not change the project's `tasks.txt`.
