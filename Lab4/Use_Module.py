from HandyMath import max, min
import HandyMath


number1 = float(input("Enter the first number: "))
number2 = float(input("Enter the second number: "))

print(f"The midpoint is {HandyMath.midpoint(number1, number2)}")
print(f"The square root of the square of {number1} is {HandyMath.squareroot(number1 ** 2)}")
print(f"{number1} raised to the power of {number2} is {HandyMath.exponent(number1, number2)}")
print(f"The larger number is {max(number1, number2)}")
print(f"The smaller number is {min(number1, number2)}")
