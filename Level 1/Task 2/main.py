"""Generate common number patterns using nested loops."""


def increasing_triangle(rows):
    """Return rows where each line counts up from 1 to its row number."""
    _validate_rows(rows)
    return [" ".join(str(number) for number in range(1, row + 1)) for row in range(1, rows + 1)]


def decreasing_triangle(rows):
    """Return rows that decrease in width from the requested row count."""
    _validate_rows(rows)
    return [" ".join(str(number) for number in range(1, row + 1)) for row in range(rows, 0, -1)]


def number_pyramid(rows):
    """Return a centered pyramid whose rows repeat their row number."""
    _validate_rows(rows)
    width = len(str(rows))
    lines = []
    for row in range(1, rows + 1):
        values = " ".join(str(row) for _ in range(row))
        lines.append(values.center(rows * (width + 1) - 1))
    return lines


def floyd_triangle(rows):
    """Return Floyd's triangle, numbering each value in sequence."""
    _validate_rows(rows)
    lines = []
    next_number = 1
    for row in range(1, rows + 1):
        values = []
        for _ in range(row):
            values.append(str(next_number))
            next_number += 1
        lines.append(" ".join(values))
    return lines


def _validate_rows(rows):
    if not isinstance(rows, int) or isinstance(rows, bool) or rows < 1:
        raise ValueError("Rows must be a positive whole number.")


PATTERNS = {
    "1": ("Increasing triangle", increasing_triangle),
    "2": ("Decreasing triangle", decreasing_triangle),
    "3": ("Number pyramid", number_pyramid),
    "4": ("Floyd's triangle", floyd_triangle),
}


def main(input_fn=input, print_fn=print):
    """Prompt for a pattern and row count, then print the formatted result."""
    print_fn("Choose a pattern:")
    for choice, (name, _) in PATTERNS.items():
        print_fn(f"{choice}. {name}")
    choice = input_fn("Pattern number: ").strip()
    if choice not in PATTERNS:
        print_fn("Invalid pattern choice. Please select 1, 2, 3, or 4.")
        return

    raw_rows = input_fn("Number of rows: ").strip()
    try:
        rows = int(raw_rows)
        _validate_rows(rows)
    except ValueError:
        print_fn("Please enter a positive whole number of rows.")
        return

    name, pattern_function = PATTERNS[choice]
    print_fn(f"\n{name} ({rows} rows):")
    for line in pattern_function(rows):
        print_fn(line)


if __name__ == "__main__":
    main()
