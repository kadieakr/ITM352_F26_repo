# For records with fares over $10, calculate the total fare, average fare,
# and maximum trip distance.

import csv
import os
import stat

filename = os.path.join(os.path.dirname(__file__), "..", "taxi_1000.csv")

if os.path.isfile(filename) and os.access(filename, os.R_OK):
    file_info = os.stat(filename)
    print(f"File size: {file_info.st_size:,} bytes")
    print(f"Permissions: {stat.filemode(file_info.st_mode)}")

    with open(filename, "r", newline="", encoding="utf-8") as file:
        csv_reader = csv.reader(file)

        total_fare = 0.0
        max_distance = None
        qualifying_rows = 0
        headers = next(csv_reader)
        fare_index = headers.index("Fare")
        distance_index = headers.index("Trip Miles")

        for row in csv_reader:
            fare = float(row[fare_index])

            if fare > 10:
                distance = float(row[distance_index])
                total_fare += fare
                qualifying_rows += 1

                if max_distance is None or distance > max_distance:
                    max_distance = distance

    if qualifying_rows:
        average_fare = total_fare / qualifying_rows
        print(f"Total fare for fares over $10: ${total_fare:.2f}")
        print(f"Average fare for fares over $10: ${average_fare:.2f}")
        print(f"Maximum trip distance for fares over $10: {max_distance:.2f} miles")
    else:
        print("No records have fares greater than $10.")
else:
    print("Cannot read the CSV: it does not exist or is not readable.")