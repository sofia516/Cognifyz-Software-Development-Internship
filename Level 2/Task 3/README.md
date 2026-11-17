# Level 2, Task 3: Console-based Task Manager

A beginner-friendly console application for creating, viewing, updating, and deleting tasks. Tasks are stored in a Python list while the program runs. Each task has an automatically assigned ID, a required title, an optional description, and a `Pending` or `Completed` status.

## Run the application

```bash
python main.py
```

Use the numbered menu to manage tasks. When updating, leave a field blank to keep its current value. Task data is held in memory and is cleared when the program exits.

## Run the tests

```bash
python -m unittest -v
```

The `TaskManager` class contains the storage and CRUD operations separately from the console menu, making it straightforward to add a different storage layer later.
