def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


while True:
    print("\nSimple Calculator")
    print("Choose an operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")

    try:
        choice = input("Choose operation (1/2/3/4/5): ")

        if choice == "5":
            print("Goodbye!")
            break

        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        if choice == "1":
            result = add(num1, num2)
            operation = "added"
        elif choice == "2":
            result = subtract(num1, num2)
            operation = "subtracted"
        elif choice == "3":
            result = multiply(num1, num2)
            operation = "multiplied"
        elif choice == "4":
            result = divide(num1, num2)
            operation = "divided"
        else:
            print("Invalid operation selection.")
            continue

        print(f"Result: {num1} {operation} by {num2} = {result}")

    except ValueError:
        print("Please enter valid numbers.")
    except ZeroDivisionError:
        print("Error: division by zero is not allowed.")
