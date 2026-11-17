# Cognifyz Technologies Software Development Internship Projects

This repository contains six completed Python projects developed as part of the Cognifyz Technologies Software Development Internship. The tasks cover beginner programming concepts, console applications, CRUD operations, file persistence, and web scraping.

## Internship Tasks

| Level | Task | Project | Highlights |
| --- | --- | --- | --- |
| Level 1 | Task 1 | Number Guessing Game | Random number, limited guesses, hints, input validation, and replay |
| Level 1 | Task 2 | Number Pattern Generator | Increasing and decreasing triangles, number pyramid, and Floyd's triangle |
| Level 2 | Task 3 | Console-Based CRUD Task Manager | Create, display, update, and delete in-memory tasks |
| Level 2 | Task 4 | Temperature Converter | Celsius/Fahrenheit conversion with validation and repeated use |
| Level 3 | Task 5 | CRUD Task Manager with File Persistence | CRUD tasks saved and loaded using JSON text-file persistence |
| Level 3 | Task 6 | Interactive Web Scraping | Book data extraction and search using `requests` and BeautifulSoup |

## Technologies Used

- Python 3
- Python standard library, including `random`, `unittest`, and JSON file handling
- `requests` for HTTP requests in Level 3, Task 6
- BeautifulSoup (`beautifulsoup4`) for HTML parsing in Level 3, Task 6

## Repository Structure

```text
.
├── Level 1/
│   ├── Task 1/       # Number Guessing Game
│   └── Task 2/       # Number Pattern Generator
├── Level 2/
│   ├── Task 3/       # In-memory CRUD Task Manager
│   └── Task 4/       # Temperature Converter
└── Level 3/
    ├── Task 5/       # CRUD Task Manager with JSON text-file persistence
    └── Task 6/       # Interactive web scraper (requests + BeautifulSoup)
```

Each task directory contains its own `main.py`, `test_main.py`, and `README.md`. Task 6 also includes a `requirements.txt`; Task 5 includes a `tasks.txt` data file.

## Setup

Install Python 3. For Level 3, Task 6, install its dependencies from that task directory:

```bash
cd "Level 3/Task 6"
python -m pip install -r requirements.txt
```

The other tasks use only the Python standard library.

## Run a Task

Run each command from the listed task directory:

```bash
# Level 1, Task 1 — Number Guessing Game
cd "Level 1/Task 1"
python main.py

# Level 1, Task 2 — Number Pattern Generator
cd "Level 1/Task 2"
python main.py

# Level 2, Task 3 — Console-Based CRUD Task Manager
cd "Level 2/Task 3"
python main.py

# Level 2, Task 4 — Temperature Converter
cd "Level 2/Task 4"
python main.py

# Level 3, Task 5 — CRUD Task Manager with File Persistence
cd "Level 3/Task 5"
python main.py

# Level 3, Task 6 — Interactive Web Scraping
cd "Level 3/Task 6"
python main.py
```

Task 5 stores task records as JSON in its local `tasks.txt` file. Task 6 fetches the Books to Scrape practice catalog using `requests` and parses book details with BeautifulSoup. Use web scraping responsibly and respect the website's terms and access policies.

## Run Tests

Run each task's tests from its own directory:

```bash
cd "Level 1/Task 1"
python -m unittest -v

cd "Level 1/Task 2"
python -m unittest -v

cd "Level 2/Task 3"
python -m unittest -v

cd "Level 2/Task 4"
python -m unittest -v

cd "Level 3/Task 5"
python -m unittest -v

cd "Level 3/Task 6"
python -m unittest -v
```

The verified combined result is **47 tests passed across six test suites**. The test suites use standard-library `unittest`; Task 6's HTTP calls are mocked in tests, so its unit tests do not depend on a live website.

## Screenshots and Demo

Add screenshots or a short demo video for the completed projects here:

- **Number Guessing Game:** `[Add screenshot or demo link]`
- **Number Pattern Generator:** `[Add screenshot or demo link]`
- **Task Managers:** `[Add screenshot or demo link]`
- **Temperature Converter:** `[Add screenshot or demo link]`
- **Interactive Web Scraping:** `[Add screenshot or demo link]`
