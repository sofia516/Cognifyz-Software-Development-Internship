"""Unit tests for parsing, searching, display limits, and request handling."""

import unittest
from unittest.mock import Mock

import requests

from main import display_books, fetch_books, parse_books, run_menu, search_books


SAMPLE_HTML = """
<html><body><ol class="row">
  <li><article class="product_pod">
    <p class="star-rating Three"></p>
    <h3><a href="book.html" title="Sample Book Title">Sample Book Title</a></h3>
    <div class="product_price"><p class="price_color">£12.34</p>
      <p class="instock availability">\n In stock \n</p></div>
  </article></li>
  <li><article class="product_pod">
    <p class="star-rating Five"></p>
    <h3><a title="Another Story">Another Story</a></h3>
    <p class="price_color">£9.99</p><p class="availability">In stock (2 available)</p>
  </article></li>
</ol></body></html>
"""


class ParsingAndDisplayTests(unittest.TestCase):
    def test_extracts_all_book_fields(self):
        books = parse_books(SAMPLE_HTML)
        self.assertEqual(books[0], {
            "title": "Sample Book Title",
            "price": "£12.34",
            "availability": "In stock",
            "rating": "3/5",
        })
        self.assertEqual(books[1]["rating"], "5/5")

    def test_missing_html_elements_use_unknown_values(self):
        books = parse_books('<article class="product_pod"><h3></h3></article>')
        self.assertEqual(books, [{
            "title": "Unknown", "price": "Unknown",
            "availability": "Unknown", "rating": "Unknown",
        }])

    def test_search_by_title_is_case_insensitive(self):
        books = parse_books(SAMPLE_HTML)
        self.assertEqual([book["title"] for book in search_books(books, "sample")], ["Sample Book Title"])
        self.assertEqual(search_books(books, "  "), [])

    def test_display_limits_results(self):
        books = parse_books(SAMPLE_HTML)
        output = []
        shown = display_books(books, 1, output.append)
        self.assertEqual(shown, 1)
        self.assertTrue(any("Sample Book Title" in line for line in output))
        self.assertFalse(any("Another Story" in line for line in output))


class FetchTests(unittest.TestCase):
    def test_fetch_uses_timeout_and_parses_response(self):
        response = Mock(text=SAMPLE_HTML)
        session = Mock()
        session.get.return_value = response
        books = fetch_books(session=session)
        session.get.assert_called_once()
        self.assertEqual(session.get.call_args.kwargs["timeout"], 10)
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(len(books), 2)

    def test_request_failure_and_timeout_propagate_for_menu_handling(self):
        for error in (requests.ConnectionError("offline"), requests.Timeout("slow")):
            with self.subTest(error=type(error).__name__):
                session = Mock()
                session.get.side_effect = error
                with self.assertRaises(type(error)):
                    fetch_books(session=session)

    def test_invalid_response_is_reported(self):
        response = Mock(text="<html><body>not a catalog</body></html>")
        session = Mock()
        session.get.return_value = response
        with self.assertRaisesRegex(ValueError, "No book listings"):
            fetch_books(session=session)


class MenuTests(unittest.TestCase):
    def test_invalid_menu_input_is_handled(self):
        answers = iter(["bad", "3"])
        output = []
        run_menu(lambda _prompt: next(answers), output.append, fetcher=lambda: [])
        self.assertTrue(any("Invalid menu choice" in line for line in output))

    def test_invalid_book_count_is_handled_and_menu_continues(self):
        answers = iter(["1", "zero", "3"])
        output = []
        run_menu(lambda _prompt: next(answers), output.append, fetcher=lambda: parse_books(SAMPLE_HTML))
        self.assertTrue(any("positive whole number" in line for line in output))
        self.assertIn("Goodbye!", output)

    def test_request_error_is_handled_without_crashing(self):
        answers = iter(["1", "3"])
        output = []
        def fail_fetch():
            raise requests.Timeout("request took too long")
        run_menu(lambda _prompt: next(answers), output.append, fetcher=fail_fetch)
        self.assertTrue(any("Could not fetch books" in line for line in output))
        self.assertIn("Goodbye!", output)


if __name__ == "__main__":
    unittest.main()
