# Read the entire file using readlines()

with open("names.txt", "r") as file_objects:
    names = file_object.readlines()
    print(f"Number of names: {len(names)}")
    for name in names:
        print(name.strip())