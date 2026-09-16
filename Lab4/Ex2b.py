"""Temperature conversion using a function passed as an argument."""


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit):
    return (fahrenheit - 32) * 5 / 9 + 273.15


def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9 / 5 + 32


def convert_temperature(temperature, conversion_function):
    return conversion_function(temperature)


print(f"25 C to Fahrenheit: {convert_temperature(25, celsius_to_fahrenheit):.2f} F")
print(f"77 F to Celsius: {convert_temperature(77, fahrenheit_to_celsius):.2f} C")
print(f"25 C to Kelvin: {convert_temperature(25, celsius_to_kelvin):.2f} K")
print(f"298.15 K to Celsius: {convert_temperature(298.15, kelvin_to_celsius):.2f} C")
print(f"77 F to Kelvin: {convert_temperature(77, fahrenheit_to_kelvin):.2f} K")
print(f"298.15 K to Fahrenheit: {convert_temperature(298.15, kelvin_to_fahrenheit):.2f} F")
