def gcd(a, b):
	"""Return the greatest common divisor using the Euclidean algorithm."""
	a = abs(a)
	b = abs(b)

	while b != 0:
		remainder = a % b
		a = b
		b = remainder

	return a


first_number = int(input("Enter the first number: "))
second_number = int(input("Enter the second number: "))

print(f"The GCD of {first_number} and {second_number} is {gcd(first_number, second_number)}.")
