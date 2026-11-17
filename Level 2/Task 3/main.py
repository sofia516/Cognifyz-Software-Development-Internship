"""Console task manager with in-memory CRUD operations."""


class Task:
    """One task with an ID, title, description, and completion status."""

    def __init__(self, task_id, title, description="", status="Pending"):
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        if status not in ("Pending", "Completed"):
            raise ValueError("Status must be Pending or Completed.")
        self.task_id = task_id
        self.title = title
        self.description = description.strip()
        self.status = status

    def __str__(self):
        return (f"[{self.task_id}] {self.title} | {self.status}\n"
                f"    {self.description or '(No description)'}")


class TaskManager:
    """Manage tasks in a list, keeping storage separate from the menu."""

    def __init__(self, tasks=None):
        self.tasks = list(tasks) if tasks is not None else []
        self._next_id = max((task.task_id for task in self.tasks), default=0) + 1

    def create_task(self, title, description=""):
        task = Task(self._next_id, title, description)
        self.tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self):
        """Return a copy so callers cannot accidentally replace stored tasks."""
        return list(self.tasks)

    def get_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        raise ValueError(f"Task ID {task_id} was not found.")

    def update_task(self, task_id, title=None, description=None, status=None):
        task = self.get_task(task_id)
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty.")
            task.title = title.strip()
        if description is not None:
            task.description = description.strip()
        if status is not None:
            normalized_status = status.strip().capitalize()
            if normalized_status not in ("Pending", "Completed"):
                raise ValueError("Status must be Pending or Completed.")
            task.status = normalized_status
        return task

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        self.tasks.remove(task)
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
    """Run the console menu; an optional manager makes the UI easy to test."""
    manager = manager or TaskManager()
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


def main():
    run_menu()


if __name__ == "__main__":
    main()
