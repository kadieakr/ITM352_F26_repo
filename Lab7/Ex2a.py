test_cases = [
    [95, "Grade: A"],
    [85, "Grade: B"],
    [75, "Grade: C"]
]

for test in test_cases:
    score = test[0]
    expected = test[1]

    if score >= 90:
        result = "Grade: A"
    elif score >= 80:
        result = "Grade: B"
    else:
        result = "Grade: C"

    print(score, result, expected, result == expected)