"""Unit tests for task creation, display, updates, deletion, and validation."""

import unittest

from main import Task, TaskManager, run_menu


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()

    def test_task_creation(self):
        task = self.manager.create_task("  Study Python  ", "Review loops")
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Study Python")
        self.assertEqual(task.description, "Review loops")
        self.assertEqual(task.status, "Pending")

    def test_display_all_tasks(self):
        self.manager.create_task("First", "One")
        self.manager.create_task("Second", "Two")
        self.assertEqual([task.title for task in self.manager.get_all_tasks()], ["First", "Second"])

    def test_update_task_details(self):
        task = self.manager.create_task("Draft", "Old description")
        updated = self.manager.update_task(task.task_id, "Final", "New description", "completed")
        self.assertEqual(updated.title, "Final")
        self.assertEqual(updated.description, "New description")
        self.assertEqual(updated.status, "Completed")

    def test_delete_task(self):
        task = self.manager.create_task("Temporary")
        deleted = self.manager.delete_task(task.task_id)
        self.assertIs(deleted, task)
        self.assertEqual(self.manager.get_all_tasks(), [])

    def test_invalid_id_is_handled(self):
        with self.assertRaisesRegex(ValueError, "not found"):
            self.manager.update_task(99, title="Missing")
        with self.assertRaisesRegex(ValueError, "not found"):
            self.manager.delete_task(99)

    def test_empty_title_is_rejected(self):
        for title in ("", "   "):
            with self.subTest(title=title):
                with self.assertRaisesRegex(ValueError, "cannot be empty"):
                    self.manager.create_task(title)

    def test_invalid_status_is_rejected(self):
        task = self.manager.create_task("Valid")
        with self.assertRaisesRegex(ValueError, "Status must be"):
            self.manager.update_task(task.task_id, status="Started")


class MenuTests(unittest.TestCase):
    def test_menu_displays_tasks_and_handles_bad_input(self):
        answers = iter(["bad", "2", "5"])
        output = []
        manager = TaskManager([Task(1, "Read", "A book")])
        run_menu(manager, lambda _prompt: next(answers), output.append)
        self.assertTrue(any("Invalid menu option" in line for line in output))
        self.assertTrue(any("[1] Read" in line for line in output))

    def test_menu_handles_invalid_task_id(self):
        answers = iter(["4", "nope", "5"])
        output = []
        run_menu(TaskManager(), lambda _prompt: next(answers), output.append)
        self.assertTrue(any("Task ID must be a whole number" in line for line in output))

    def test_menu_prevents_empty_title(self):
        answers = iter(["1", "   ", "Description", "5"])
        output = []
        run_menu(TaskManager(), lambda _prompt: next(answers), output.append)
        self.assertTrue(any("Task title cannot be empty" in line for line in output))


if __name__ == "__main__":
    unittest.main()
