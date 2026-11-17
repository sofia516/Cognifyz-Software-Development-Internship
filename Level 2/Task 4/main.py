"""Menu-driven Celsius and Fahrenheit converter."""


def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def _parse_temperature(raw_value):
    """Parse a numeric temperature while rejecting blank and non-finite values."""
    try:
        value = float(raw_value.strip())
    except (ValueError, AttributeError) as error:
        raise ValueError("Please enter a valid numeric temperature.") from error
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError("Please enter a finite numeric temperature.")
    return value


def run_menu(input_fn=input, print_fn=print):
    """Perform conversions repeatedly until the user chooses to exit."""
    while True:
        print_fn("\nTemperature Converter")
        print_fn("1. Celsius to Fahrenheit")
        print_fn("2. Fahrenheit to Celsius")
        print_fn("3. Exit")
        choice = input_fn("Choose an option: ").strip()

        if choice == "3":
            print_fn("Goodbye!")
            return
        if choice not in ("1", "2"):
            print_fn("Invalid menu choice. Select 1, 2, or 3.")
            continue

        raw_temperature = input_fn("Enter the temperature: ")
        try:
            temperature = _parse_temperature(raw_temperature)
        except ValueError as error:
            print_fn(str(error))
            continue

        if choice == "1":
            converted = celsius_to_fahrenheit(temperature)
            print_fn(f"{temperature:g} °C = {converted:.2f} °F")
        else:
            converted = fahrenheit_to_celsius(temperature)
            print_fn(f"{temperature:g} °F = {converted:.2f} °C")


def main():
    run_menu()


if __name__ == "__main__":
    main()
