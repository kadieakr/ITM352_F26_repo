birth_year = 2005

# Leap-year rule:
# (divisible by 4 and not divisible by 100) OR divisible by 400
is_leap_year = ((birth_year % 4 == 0 and birth_year % 100 != 0) or (birth_year % 400 == 0))

if is_leap_year:
    test_year = birth_year + 1
    nearest_leap_year = birth_year
else:
    test_year = birth_year
    nearest_leap_year = birth_year + 1

for year in [birth_year, nearest_leap_year, test_year]:
    is_leap = ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0))

    if is_leap:
        print(f"{year} is a leap year.")
    else:
        print(f"{year} is not a leap year.")


