"""Command-line sales dashboard backed by a Google Drive CSV."""

import re
import sys
import time
from typing import Literal, cast

import pandas as pd


SALES_DATA_URL = (
	"https://drive.google.com/uc?export=download&"
	"id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
)

# These fields are used by the sales analytics in the course example:
# date/quantity/price for sales totals, plus region and order type for breakdowns.
REQUIRED_FIELDS = {
	"order_date",
	"quantity",
	"unit_price",
	"sales_region",
	"order_type",
	"customer_type",
	"customer_state",
	"product_category",
	"employee_id",
}


def normalize_column_name(column_name):
	"""Normalize spaces and punctuation so equivalent header styles match."""
	return re.sub(r"[^a-z0-9]+", "_", str(column_name).strip().lower()).strip("_")


def load_sales_data():
	"""Load the shared Google Drive CSV and report its schema and row count."""
	print("Loading sales_data.csv from Google Drive...", flush=True)
	start_time = time.perf_counter()

	try:
		sales_df = pd.read_csv(SALES_DATA_URL)
	except Exception as error:
		print(
			"Error: Could not load sales_data.csv from Google Drive. "
			"Check your internet connection and confirm the file is shared "
			f"for access. Details: {error}",
			file=sys.stderr,
		)
		raise SystemExit(1) from error

	load_time = time.perf_counter() - start_time
	sales_df = sales_df.fillna(0)
	for column in ("quantity", "unit_price"):
		if column in sales_df.columns:
			sales_df[column] = pd.to_numeric(sales_df[column], errors="coerce").fillna(0)

	if {"quantity", "unit_price"}.issubset(sales_df.columns):
		sales_df["sales"] = sales_df["quantity"] * sales_df["unit_price"]

	print(f"Successfully loaded sales_data.csv in {load_time:.2f} seconds.")
	print(f"Rows of data: {len(sales_df):,}")
	print("Available columns: " + ", ".join(map(str, sales_df.columns)))

	normalized_columns = {normalize_column_name(column) for column in sales_df.columns}
	missing_fields = sorted(REQUIRED_FIELDS - normalized_columns)
	if missing_fields:
		print(
			"Warning: The dataset is missing required field(s): "
			f"{', '.join(missing_fields)}. Some dashboard analytics may not work."
		)
	else:
		print("All required fields for the dashboard analytics are available.")

	return sales_df


def get_column(sales_df, normalized_name):
	"""Return the original dataframe column matching a normalized name."""
	return next(
		(column for column in sales_df.columns if normalize_column_name(column) == normalized_name),
		None,
	)


def show_table(table):
	"""Print an analytics table in a readable command-line format."""
	if table.empty:
		print("No data is available for this analysis.")
	else:
		print(table.to_string(index=False))


def first_rows(sales_df):
	"""Display the first n rows requested by the user."""
	while True:
		try:
			num_rows = int(input("How many rows should be displayed? "))
			if num_rows < 0:
				print("Enter zero or a positive number.")
				continue
			break
		except ValueError:
			print("Enter a whole number.")
	show_table(sales_df.head(num_rows))


def total_sales_by_region_order_type(sales_df):
	"""Show total revenue by region and order type."""
	grouped_sales(sales_df, ["sales_region", "order_type"], "sum")


def average_sales_by_region_state_type(sales_df):
	"""Show average revenue by region, state, and order type."""
	grouped_sales(
		sales_df,
		["sales_region", "customer_state", "order_type"],
		"mean",
		value_label="average_sales",
	)


def sales_by_customer_type_order_type_state(sales_df):
	"""Show total revenue by customer type, order type, and state."""
	grouped_sales(sales_df, ["customer_type", "order_type", "customer_state"], "sum")


def total_quantity_and_sales_by_region_product(sales_df):
	"""Show total quantity and revenue by region and product."""
	region_column = get_column(sales_df, "sales_region")
	product_column = None
	for field in ("produce_name", "product_name", "product_number"):
		product_column = get_column(sales_df, field)
		if product_column is not None:
			break
	quantity_column = get_column(sales_df, "quantity")
	if region_column is None or product_column is None or quantity_column is None:
		missing = [
			name
			for name, column in (
				("sales_region", region_column),
				("product name/number", product_column),
				("quantity", quantity_column),
			)
			if column is None
		]
		print("Cannot run this analysis; missing: " + ", ".join(missing))
		return
	if "sales" not in sales_df.columns:
		print("Cannot run this analysis; quantity and unit_price are required to calculate sales.")
		return
	result = (
		sales_df.groupby([region_column, product_column], dropna=False)
		.agg(total_quantity=(quantity_column, "sum"), total_sales=("sales", "sum"))
		.reset_index()
	)
	show_table(result)


def total_quantity_and_sales_by_customer_type(sales_df):
	"""Show total quantity and revenue by customer type."""
	customer_column = get_column(sales_df, "customer_type")
	quantity_column = get_column(sales_df, "quantity")
	if customer_column is None or quantity_column is None or "sales" not in sales_df.columns:
		print("Cannot run this analysis; customer_type, quantity, and unit_price are required.")
		return
	result = (
		sales_df.groupby(customer_column, dropna=False)
		.agg(total_quantity=(quantity_column, "sum"), total_sales=("sales", "sum"))
		.reset_index()
	)
	show_table(result)


def max_min_sales_price_by_category(sales_df):
	"""Show the minimum and maximum unit price for each product category."""
	category_column = get_column(sales_df, "product_category")
	price_column = get_column(sales_df, "unit_price")
	if category_column is None or price_column is None:
		print("Cannot run this analysis; product_category and unit_price are required.")
		return
	result = (
		sales_df.groupby(category_column, dropna=False)[price_column]
		.agg(min_price="min", max_price="max")
		.reset_index()
	)
	show_table(result)


def unique_employees_by_region(sales_df):
	"""Show the number of unique employees in each sales region."""
	region_column = get_column(sales_df, "sales_region")
	employee_column = get_column(sales_df, "employee_id")
	if region_column is None or employee_column is None:
		print("Cannot run this analysis; sales_region and employee_id are required.")
		return
	result = (
		sales_df.groupby(region_column, dropna=False)[employee_column]
		.nunique()
		.rename("unique_employees")
		.reset_index()
	)
	show_table(result)


def custom_pivot_table(sales_df):
	"""Build a pivot table from user-selected fields and aggregation."""
	columns = list(sales_df.columns)
	if "sales" not in columns and {"quantity", "unit_price"}.issubset(sales_df.columns):
		columns.append("sales")
	print("Available fields: " + ", ".join(map(str, columns)))
	index_field = input("Row field: ").strip()
	column_field = input("Column field (leave blank for none): ").strip()
	value_field = input("Value field: ").strip()
	aggregation = input("Aggregation (sum, mean, min, max, count): ").strip().lower()
	allowed_aggregations = {"sum", "mean", "min", "max", "count"}
	if index_field not in columns or value_field not in columns:
		print("Row and value fields must match an available field exactly.")
		return
	if column_field and column_field not in columns:
		print("Column field must match an available field exactly.")
		return
	if aggregation not in allowed_aggregations:
		print("Choose one of: " + ", ".join(sorted(allowed_aggregations)))
		return
	aggregation = cast(Literal["sum", "mean", "min", "max", "count"], aggregation)
	try:
		pivot = pd.pivot_table(
			sales_df,
			index=index_field,
			columns=column_field or None,
			values=value_field,
			aggfunc=aggregation,
			fill_value=0,
		)
		print(pivot.to_string())
	except (KeyError, TypeError, ValueError) as error:
		print(f"Could not create the pivot table: {error}")


def exit_dashboard(_sales_df):
	"""Signal that the dashboard should exit."""
	print("Goodbye.")
	return False


def grouped_sales(sales_df, group_fields, aggregation, value_label="total_sales"):
	"""Aggregate the calculated sales measure by requested fields."""
	if "sales" not in sales_df.columns:
		print("Cannot run this analysis; quantity and unit_price are required to calculate sales.")
		return
	columns = [get_column(sales_df, field) for field in group_fields]
	missing = [field for field, column in zip(group_fields, columns) if column is None]
	if missing:
		print("Cannot run this analysis; missing: " + ", ".join(missing))
		return
	result = (
		sales_df.groupby(columns, dropna=False)["sales"]
		.agg(aggregation)
		.rename(value_label)
		.reset_index()
	)
	show_table(result)


MENU_ITEMS = (
	("Show the first n rows of sales data", first_rows),
	("Total sales by region and order_type", total_sales_by_region_order_type),
	("Average sales by region, state, and order type", average_sales_by_region_state_type),
	("Sales by customer type and order type by state", sales_by_customer_type_order_type_state),
	("Total sales quantity and price by region and product", total_quantity_and_sales_by_region_product),
	("Total sales quantity and price by customer type", total_quantity_and_sales_by_customer_type),
	("Max and min sales price by category", max_min_sales_price_by_category),
	("Number of unique employees by region", unique_employees_by_region),
	("Create a custom pivot table", custom_pivot_table),
	("Exit", exit_dashboard),
)


def run_dashboard(sales_df):
	"""Display the tuple-defined menu and dispatch the selected function."""
	while True:
		print("\n--- Sales Data Dashboard ---")
		for number, (description, _function) in enumerate(MENU_ITEMS, start=1):
			print(f"#{number}. {description}")
		try:
			selection = int(input("Select an option: "))
		except ValueError:
			print("Enter the number of a menu option.")
			continue
		if not 1 <= selection <= len(MENU_ITEMS):
			print(f"Choose a number from 1 to {len(MENU_ITEMS)}.")
			continue
		if MENU_ITEMS[selection - 1][1](sales_df) is False:
			break


if __name__ == "__main__":
	sales_data = load_sales_data()
	run_dashboard(sales_data)
