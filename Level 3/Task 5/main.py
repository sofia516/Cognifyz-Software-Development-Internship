"""Console task manager with simple JSON text-file persistence."""

import json
from pathlib import Path


class Task:
    """One task with an ID, title, description, and completion status."""

    def __init__(self, task_id, title, description="", status="Pending"):
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        if not isinstance(task_id, int) or isinstance(task_id, bool) or task_id < 1:
            raise ValueError("Task ID must be a positive whole number.")
        if status not in ("Pending", "Completed"):
            raise ValueError("Status must be Pending or Completed.")
        self.task_id = task_id
        self.title = title
        self.description = description.strip()
        self.status = status

    def __str__(self):
        return (f"[{self.task_id}] {self.title} | {self.status}\n"
                f"    {self.description or '(No description)'}")

    def to_record(self):
        """Return a plain dictionary that can be written as JSON."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
        }


class TaskManager:
    """Manage an in-memory list and save it to a local text file."""

    def __init__(self, data_file=None, tasks=None):
        self.data_file = Path(data_file) if data_file is not None else Path(__file__).with_name("tasks.txt")
        self.tasks = list(tasks) if tasks is not None else []
        self.load_error = None
        self.persistence_error = None
        if tasks is None:
            self.load_tasks()
        self._next_id = max((task.task_id for task in self.tasks), default=0) + 1

    def load_tasks(self):
        """Load valid task records; a missing file starts as an empty list."""
        try:
            with self.data_file.open("r", encoding="utf-8") as task_file:
                records = json.load(task_file)
        except FileNotFoundError:
            self.tasks = []
            self.save_tasks()  # Create the empty local data file on first start.
            return self.tasks
        except (OSError, json.JSONDecodeError) as error:
            self.tasks = []
            self.load_error = f"Could not load task data: {error}"
            return self.tasks

        if not isinstance(records, list):
            self.tasks = []
            self.load_error = "Could not load task data: expected a list of tasks."
            return self.tasks

        loaded = []
        seen_ids = set()
        skipped = 0
        for record in records:
            try:
                if not isinstance(record, dict):
                    raise ValueError("Task record must be an object.")
                task = Task(
                    record["task_id"],
                    record["title"],
                    record.get("description", ""),
                    record.get("status", "Pending"),
                )
                if task.task_id in seen_ids:
                    raise ValueError("Duplicate task ID.")
                seen_ids.add(task.task_id)
                loaded.append(task)
            except (KeyError, TypeError, AttributeError, ValueError):
                skipped += 1
        self.tasks = loaded
        if skipped:
            self.load_error = f"Skipped {skipped} invalid task record(s) in the data file."
        return self.tasks

    def save_tasks(self):
        """Write all current tasks; report an error instead of crashing."""
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            with self.data_file.open("w", encoding="utf-8") as task_file:
                json.dump([task.to_record() for task in self.tasks], task_file, indent=2)
                task_file.write("\n")
        except OSError as error:
            self.persistence_error = f"Could not save task data: {error}"
            return False
        self.persistence_error = None
        return True

    def create_task(self, title, description=""):
        task = Task(self._next_id, title, description)
        self.tasks.append(task)
        self._next_id += 1
        self.save_tasks()
        return task

    def get_all_tasks(self):
        """Return a copy so callers cannot replace stored tasks accidentally."""
        return list(self.tasks)

    def get_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        raise ValueError(f"Task ID {task_id} was not found.")

    def update_task(self, task_id, title=None, description=None, status=None):
        task = self.get_task(task_id)
        # Validate every requested change before modifying the stored object.
        new_title = task.title if title is None else title.strip()
        new_description = task.description if description is None else description.strip()
        new_status = task.status if status is None else status.strip().capitalize()
        if not new_title:
            raise ValueError("Task title cannot be empty.")
        if new_status not in ("Pending", "Completed"):
            raise ValueError("Status must be Pending or Completed.")
        task.title = new_title
        task.description = new_description
        task.status = new_status
        self.save_tasks()
        return task

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        self.tasks.remove(task)
        self.save_tasks()
        return task


def _read_task_id(input_fn):
    raw_id = input_fn("Task ID: ").strip()
    try:
        task_id = int(raw_id)
    except ValueError as error:
        raise ValueError("Task ID must be a whole number.") from error
    if task_id < 1:
        raise ValueError("Task ID must be a positive whole number.")
    return task_id


def run_menu(manager=None, input_fn=input, print_fn=print):
    """Run the menu with an optional manager and injectable console functions."""
    manager = manager or TaskManager()
    if manager.load_error:
        print_fn(f"Warning: {manager.load_error}")
    if manager.persistence_error:
        print_fn(f"Warning: {manager.persistence_error}")

    while True:
        print_fn("\nTask Manager")
        print_fn("1. Create task")
        print_fn("2. Display all tasks")
        print_fn("3. Update task")
        print_fn("4. Delete task")
        print_fn("5. Exit")
        choice = input_fn("Choose an option: ").strip()

        try:
            if choice == "1":
                title = input_fn("Title: ")
                description = input_fn("Description: ")
                task = manager.create_task(title, description)
                print_fn(f"Created task {task.task_id}.")
            elif choice == "2":
                tasks = manager.get_all_tasks()
                if not tasks:
                    print_fn("No tasks yet.")
                else:
                    for task in tasks:
                        print_fn(str(task))
            elif choice == "3":
                task_id = _read_task_id(input_fn)
                current = manager.get_task(task_id)
                print_fn("Leave a field blank to keep its current value.")
                title = input_fn(f"Title [{current.title}]: ")
                description = input_fn(f"Description [{current.description}]: ")
                status = input_fn(f"Status (Pending/Completed) [{current.status}]: ")
                manager.update_task(
                    task_id,
                    title=title if title.strip() else None,
                    description=description if description.strip() else None,
                    status=status if status.strip() else None,
                )
                print_fn("Task updated.")
            elif choice == "4":
                task_id = _read_task_id(input_fn)
                manager.delete_task(task_id)
                print_fn("Task deleted.")
            elif choice == "5":
                print_fn("Goodbye!")
                return manager
            else:
                print_fn("Invalid menu option. Choose a number from 1 to 5.")
        except ValueError as error:
            print_fn(f"Error: {error}")

        if manager.persistence_error:
            print_fn(f"Warning: {manager.persistence_error}")


def main():
    run_menu()


if __name__ == "__main__":
    main()
