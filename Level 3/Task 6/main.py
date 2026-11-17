"""Interactive practice scraper for the Books to Scrape catalog."""

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
REQUEST_TIMEOUT = 10
RATING_NAMES = {"One": "1/5", "Two": "2/5", "Three": "3/5", "Four": "4/5", "Five": "5/5"}


def parse_books(html):
    """Extract book details from one catalog page, using Unknown for missing fields."""
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for article in soup.select("article.product_pod"):
        title_element = article.select_one("h3 a")
        price_element = article.select_one(".price_color")
        availability_element = article.select_one(".availability")
        rating_element = article.select_one(".star-rating")

        title = title_element.get("title", "").strip() if title_element else "Unknown"
        price = price_element.get_text(" ", strip=True) if price_element else "Unknown"
        availability = availability_element.get_text(" ", strip=True) if availability_element else "Unknown"
        rating = "Unknown"
        if rating_element:
            rating_class = next(
                (class_name for class_name in rating_element.get("class", [])
                 if class_name in RATING_NAMES),
                None,
            )
            if rating_class:
                rating = RATING_NAMES[rating_class]

        books.append({
            "title": title or "Unknown",
            "price": price or "Unknown",
            "availability": availability or "Unknown",
            "rating": rating,
        })
    return books


def fetch_books(url=BASE_URL, session=requests):
    """Fetch one catalog page with a timeout, then parse its books."""
    response = session.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    html = response.text
    if not html or not html.strip():
        raise ValueError("The website returned an empty response.")
    books = parse_books(html)
    if not books:
        raise ValueError("No book listings were found in the webpage response.")
    return books


def search_books(books, title_query):
    """Return books whose title contains the query, ignoring letter case."""
    query = title_query.strip().casefold()
    if not query:
        return []
    return [book for book in books if query in book["title"].casefold()]


def display_books(books, limit=None, print_fn=print):
    """Print up to limit books in a readable format and return the count shown."""
    selected = books if limit is None else books[:limit]
    if not selected:
        print_fn("No matching books found.")
        return 0
    for index, book in enumerate(selected, start=1):
        print_fn(f"{index}. {book['title']}")
        print_fn(f"   Price: {book['price']}")
        print_fn(f"   Availability: {book['availability']}")
        print_fn(f"   Rating: {book['rating']}")
    return len(selected)


def _read_positive_count(input_fn):
    """Ask for a positive whole number and reject malformed counts."""
    raw_count = input_fn("How many books should be displayed? ").strip()
    try:
        count = int(raw_count)
    except ValueError as error:
        raise ValueError("Enter a positive whole number.") from error
    if count < 1:
        raise ValueError("Enter a positive whole number.")
    return count


def run_menu(input_fn=input, print_fn=print, fetcher=fetch_books):
    """Run the interactive menu; fetcher can be replaced in tests."""
    while True:
        print_fn("\nBooks to Scrape")
        print_fn("1. Scrape and display books")
        print_fn("2. Search books by title")
        print_fn("3. Exit")
        choice = input_fn("Choose an option: ").strip()

        if choice == "3":
            print_fn("Goodbye!")
            return
        if choice not in ("1", "2"):
            print_fn("Invalid menu choice. Select 1, 2, or 3.")
            continue

        try:
            books = fetcher()
            if choice == "1":
                count = _read_positive_count(input_fn)
                shown = display_books(books, count, print_fn)
                print_fn(f"Displayed {shown} book(s) from the first catalog page.")
            else:
                query = input_fn("Enter a title or part of a title: ").strip()
                matches = search_books(books, query)
                if not matches:
                    print_fn("No matching books found.")
                else:
                    display_books(matches, print_fn=print_fn)
        except requests.RequestException as error:
            print_fn(f"Could not fetch books: {error}")
        except (ValueError, TypeError) as error:
            print_fn(f"Could not process the webpage: {error}")


def main():
    run_menu()


if __name__ == "__main__":
    main()
