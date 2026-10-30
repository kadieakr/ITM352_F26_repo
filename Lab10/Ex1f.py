# Open names.txt and read its contents
# Append a new name at the end of the file

with open("names,txt", "r") as file_objects:
    contents_list = file_object.readlines()
    print(contents_list)

with open("names.txt", "a") as file_object:
    print("Appending a new name to the file...")
    file_objects.write("Doe,John\n")

