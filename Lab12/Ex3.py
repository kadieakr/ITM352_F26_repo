# Create a dataframe from a CSV file and create a pivot table aggregating sales by region and order_type.
# Name: Kadie Kron
# Date: Oct. 30, 2026

import pandas as pd
import numpy as np
import ssl

# Ignore SSL certificate error
ssl._create_default_https_context = ssl._create_unverified_context
# Tell pandas to print all columns when displaying a Dataframe
pd.set_option("display.max_columns", None)
pd.set_option('display')

csv_file = "https://drive.google.com/uc?export=download&id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

try:
    df = pd.read_csv(csv_file, engine= "pyarrow", on_bad_lines = "skip")
    df["order date"] = pd.to_datetime(df["order_date"], errors= "coerce")
    print(df.head())

    #Calculate sales total per row
    df["sales"] = df["quantity"] * df["unit_price"]

    #Create a pivottable aggregating sales by region and order type
    pivot_table = pd.pivot_table(df,
                                 values='sales',
                                 index= 'sales region',
                                 columns= ['customer_type', 'order_type'],
                                 aggfunc="mean",
                                 margins = True,
                                 margins_name= 'Avg Sales')

print(pivot_table)
