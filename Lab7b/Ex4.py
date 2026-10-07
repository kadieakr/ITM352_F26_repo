def check_purchases(purchases, budget):
    """Return each purchase's budget status, stopping at the first over-budget purchase."""
    total_spent = 0
    results = []

    for purchase in purchases:
        total_spent += purchase
        if total_spent > budget:
            results.append((purchase, "over budget"))
            break
        results.append((purchase, "within budget"))

    return results


test_cases = [
    ([10, 20], 60, [(10, "within budget"), (20, "within budget")]),
    ([36, 24, 10], 60, [(36, "within budget"), (24, "within budget"), (10, "over budget")]),
    ([70, 10], 60, [(70, "over budget")]),
]

for purchases, budget, expected in test_cases:
    actual = check_purchases(purchases, budget)
    assert actual == expected, f"For {purchases}, expected {expected}, got {actual}"
    print(f"PASS: {purchases} with budget {budget}")


recent_purchases = [36.13, 23.87, 183.35, 22.93, 11.62]
for purchase, status in check_purchases(recent_purchases, 60):
    print(f"This purchase {purchase} is {status}.")
