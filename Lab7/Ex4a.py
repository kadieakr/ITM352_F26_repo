def isLeapYear(year):
    if year <= 0:
        return "Not a leap year."

    if year % 400 == 0:
        return "Leap year"
    elif year % 100 == 0:
        return "Not a leap year"
    elif year % 4 == 0:
        return "Leap year"
    else:
        return "Not a leap year"


birth_year = 2005
nearest_leap_year = 2004
non_leap_year = 2005

# Test with your birth year and the closest leap year
for test_year in [birth_year, nearest_leap_year, non_leap_year]:
    print(f"{test_year}: {isLeapYear(test_year)}")
