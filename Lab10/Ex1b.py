#Open file using "with"

with open("names.txt", "r") as file_object:
    print(type(file_object))

print("file is closed", file_object.closed)
