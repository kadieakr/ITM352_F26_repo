# Define a list of survey response values (5,7,3,9) and store them
# in a variable, Define a tuple of response ID's (1012, 1035, 1021, and 1053).
# and add these to the list.

response_values = [5, 7, 3, 9]
response_values.sort()
response_ids = (1012, 1035, 1021, 1053)
response_values.append(response_ids)

print("Combined response values and IDs:", response_values)

response_values.new= ((1012,5), (1035,7), (1021,3), (1053,9))
print("Combined response values and IDs:", response_values.new)
