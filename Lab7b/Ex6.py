data = ("hello", 10, "goodbye", 3, "goodnight", 5)

user_input = input("Enter an item to add to the tuple: ")
data = list(data)
data.append(user_input)
data = tuple(data)

print(data)
