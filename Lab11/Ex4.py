# Read a json file of taxi trip data and create a dataframe and some simple stats
import pandas as pd

# Read the JSON file into a Dataframe
results_df = pd.read_json("Taxi_Trips.json")

#Display the first few rows of the Dataframe
print(results_df.head(6))

#Display the first few rows of the Dataframe
print(results_df.describe())

median = results_df("Fare").median()
print("The median fare value is:", median)
