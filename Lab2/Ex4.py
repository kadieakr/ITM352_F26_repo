input_value = input("Enter a floating point number: ")
float_value = float(input_value)
squared_value = float_value ** 2
rounded_value = round(float_value, 2)
rounded_squared_value = round(squared_value, 2)
print("You entered:", rounded_value)
print("The square of the number you entered is:", rounded_squared_value)