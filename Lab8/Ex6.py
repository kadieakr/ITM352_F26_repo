searchMe = [2, 5, 7, 11, 15, 22, 27, 30, 34, 41, 55, 57, 58, 60, 77]


def contains_number(numbers, target):
	"""Return True if target appears in numbers; otherwise return False."""
	for number in numbers:
		if number == target:
			return True
	return False


user_number = int(input("Enter a number to search for: "))

if contains_number(searchMe, user_number):
	print(f"{user_number} exists in the array.")
else:
	print(f"{user_number} does not exist in the array.")

