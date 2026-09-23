email = input("Enter your email address: ")

username,domain = email.split("@")  # Split the email into username and domain

print("Username:", username)
print("Domain:", domain)


email = input("Enter your email address: ")
at_index = email.index("@")

username = email[:at_index]
domain = email[at_index + 1:]

print("Username:", username)
print("Domain:", domain)