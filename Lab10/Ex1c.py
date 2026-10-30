# Open a file and read its contents

with open("names.txt", "r") as file_object:
    contents = file_object.read()
    print(contents)
    print(f"number of names: {len(contents_list)}")
    for name in contents_list:
        print(name)
        

