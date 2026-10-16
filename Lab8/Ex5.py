def is_palindrome(text):
	"""Return True if text reads the same forwards and backwards."""
	return text == text[::-1]


user_text = input("Enter a string: ")

if is_palindrome(user_text):
	print(f"{user_text!r} is a palindrome.")
else:
	print(f"{user_text!r} is not a palindrome.")
