for number in range(1, 11):
    if number == 5:
        print("Skipping 5")
        continue
    if number == 8:
        print("Stopping")
        break
    print(number)
