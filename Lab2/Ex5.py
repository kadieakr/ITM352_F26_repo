# This program prompts the user to enter a string and then displays the string along with its length.
# Name: Kadie Kron
# Date: Sept. 4, 2026

user_string=input("Enter a string:")
string_length=len(user_string)

print("You entered:", user_string)
print("The length of the string you entered is:", string_length)

if string_length > 20:
    print("Your sentence is longer than 20 characters.")
else:
    print("Your sentence is 20 characters or less.")