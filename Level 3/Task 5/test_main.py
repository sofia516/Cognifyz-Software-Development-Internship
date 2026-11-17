"""Tests for task CRUD behavior and file persistence."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import Task, TaskManager, run_menu


class PersistentTaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "tasks.txt"
        self.manager = TaskManager(self.data_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_and_save_task(self):
        task = self.manager.create_task("Study Python", "Review file I/O")
        saved = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.assertEqual(task.task_id, 1)
        self.assertEqual(saved[0]["title"], "Study Python")
        self.assertEqual(saved[0]["status"], "Pending")

    def test_load_tasks_after_restart(self):
        self.manager.create_task("Persisted", "Keep this task")
        restarted = TaskManager(self.data_file)
        self.assertEqual(restarted.get_all_tasks()[0].title, "Persisted")
        self.assertEqual(restarted.create_task("Next").task_id, 2)

    def test_update_and_delete_are_persisted(self):
        task = self.manager.create_task("Old title", "Old description")
        self.manager.update_task(task.task_id, "New title", "New description", "Completed")
        updated_manager = TaskManager(self.data_file)
        updated = updated_manager.get_task(task.task_id)
        self.assertEqual((updated.title, updated.description, updated.status),
                         ("New title", "New description", "Completed"))
        updated_manager.delete_task(task.task_id)
        self.assertEqual(TaskManager(self.data_file).get_all_tasks(), [])

    def test_missing_file_starts_empty_and_is_created(self):
        missing_file = Path(self.temp_dir.name) / "nested" / "new_tasks.txt"
        manager = TaskManager(missing_file)
        self.assertEqual(manager.get_all_tasks(), [])
        self.assertTrue(missing_file.exists())
        self.assertEqual(json.loads(missing_file.read_text(encoding="utf-8")), [])

    def test_invalid_or_corrupted_contents_are_handled(self):
        self.data_file.write_text("not valid JSON", encoding="utf-8")
        manager = TaskManager(self.data_file)
        self.assertEqual(manager.get_all_tasks(), [])
        self.assertIn("Could not load", manager.load_error)

        self.data_file.write_text(json.dumps([
            {"task_id": 1, "title": "Good", "description": "ok", "status": "Pending"},
            {"task_id": 2, "title": "   ", "description": "bad", "status": "Pending"},
        ]), encoding="utf-8")
        manager = TaskManager(self.data_file)
        self.assertEqual([task.title for task in manager.get_all_tasks()], ["Good"])
        self.assertIn("Skipped 1", manager.load_error)

    def test_read_access_error_is_graceful(self):
        with patch("pathlib.Path.open", side_effect=PermissionError("denied")):
            manager = TaskManager(self.data_file)
        self.assertEqual(manager.get_all_tasks(), [])
        self.assertIn("Could not load", manager.load_error)

    def test_write_access_error_is_graceful(self):
        with patch("pathlib.Path.open", side_effect=PermissionError("denied")):
            manager = TaskManager(self.data_file)
            task = manager.create_task("Still available in memory")
        self.assertEqual(task.title, "Still available in memory")
        self.assertIn("Could not save", manager.persistence_error)

    def test_existing_crud_and_validation(self):
        task = self.manager.create_task("First")
        self.assertEqual(self.manager.get_all_tasks(), [task])
        self.manager.update_task(task.task_id, title="Changed")
        self.assertEqual(self.manager.get_task(task.task_id).title, "Changed")
        self.manager.delete_task(task.task_id)
        self.assertEqual(self.manager.get_all_tasks(), [])
        with self.assertRaisesRegex(ValueError, "not found"):
            self.manager.delete_task(100)
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            self.manager.create_task("  ")


class MenuTests(unittest.TestCase):
    def test_menu_reports_invalid_task_id_and_persistence_error(self):
        with tempfile.TemporaryDirectory() as folder:
            manager = TaskManager(Path(folder) / "tasks.txt")
            answers = iter(["4", "bad", "5"])
            output = []
            run_menu(manager, lambda _prompt: next(answers), output.append)
            self.assertTrue(any("Task ID must be a whole number" in line for line in output))

    def test_menu_keeps_running_after_save_error(self):
        with tempfile.TemporaryDirectory() as folder:
            manager = TaskManager(Path(folder) / "tasks.txt")
            answers = iter(["1", "Title", "Description", "5"])
            output = []
            with patch.object(manager, "save_tasks", return_value=False):
                manager.persistence_error = "Could not save task data: denied"
                run_menu(manager, lambda _prompt: next(answers), output.append)
            self.assertIn("Goodbye!", output)


if __name__ == "__main__":
    unittest.main()
