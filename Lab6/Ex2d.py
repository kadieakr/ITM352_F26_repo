trips = [
	{"miles": 1.1, "fare": 6.25},
	{"miles": 0.8, "fare": 5.25},
	{"miles": 2.5, "fare": 10.50},
	{"miles": 2.6, "fare": 8.05}
]

print(trips)
third_trip = trips[2]
print("The duration of the 3rd trip is:", third_trip["miles"], "miles")
print(f"The cost of the 3rd trip is: ${third_trip['fare']:.2f}")
