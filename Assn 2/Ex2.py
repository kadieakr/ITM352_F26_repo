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


def show_pivot_table(table):
	"""Print a pivot table while preserving its row and column labels."""
	if table.empty:
		print("No data is available for this analysis.")
	else:
		print(table.to_string())


def first_rows(sales_df):
	"""Display the first n rows, all rows, or skip the preview."""
	available_rows = len(sales_df)
	print(f"Rows available: {available_rows}")
	print("Enter rows to display:")
	if available_rows:
		print(f"- Enter a number 1 to {available_rows}")
	else:
		print("- No data rows are available")
	print("- To see all rows, enter 'all'")
	print("- To skip preview, press Enter")

	while True:
		choice = input("Your choice: ").strip()
		if not choice:
			print("Preview skipped.")
			return
		if choice.lower() == "all":
			show_table(sales_df)
			return
		try:
			num_rows = int(choice)
		except ValueError:
			print(f"Invalid choice. Enter a number from 1 to {available_rows}, 'all', or press Enter.")
			continue
		if not 1 <= num_rows <= available_rows:
			print(f"Invalid number. Enter a number from 1 to {available_rows}, 'all', or press Enter.")
			continue
		show_table(sales_df.head(num_rows))
		return


def total_sales_by_region_order_type(sales_df):
	"""Pivot total sales by region and order type."""
	region_column = get_column(sales_df, "sales_region")
	order_column = get_column(sales_df, "order_type")
	if region_column is None or order_column is None or "sales" not in sales_df.columns:
		print("Cannot run this analysis; sales_region, order_type, and sales are required.")
		return
	pivot = pd.pivot_table(
		sales_df,
		index=region_column,
		columns=order_column,
		values="sales",
		aggfunc="sum",
		fill_value=0,
	)
	show_pivot_table(pivot)


def average_sales_by_region_state_type(sales_df):
	"""Pivot average sales by region, with state and order type sub-columns."""
	region_column = get_column(sales_df, "sales_region")
	state_column = get_column(sales_df, "customer_state")
	order_column = get_column(sales_df, "order_type")
	if None in (region_column, state_column, order_column) or "sales" not in sales_df.columns:
		print("Cannot run this analysis; sales_region, customer_state, order_type, and sales are required.")
		return
	pivot = pd.pivot_table(
		sales_df,
		index=region_column,
		columns=[state_column, order_column],
		values="sales",
		aggfunc="mean",
		fill_value=0,
	)
	show_pivot_table(pivot)


def sales_by_customer_type_order_type_state(sales_df):
	"""Pivot total sales by state with customer and order-type sub-rows."""
	state_column = get_column(sales_df, "customer_state")
	customer_column = get_column(sales_df, "customer_type")
	order_column = get_column(sales_df, "order_type")
	if None in (state_column, customer_column, order_column) or "sales" not in sales_df.columns:
		print("Cannot run this analysis; state, customer_type, order_type, and sales are required.")
		return
	pivot = pd.pivot_table(
		sales_df,
		index=[state_column, customer_column, order_column],
		values="sales",
		aggfunc="sum",
		fill_value=0,
	)
	show_pivot_table(pivot)


def total_quantity_and_sales_by_region_product(sales_df):
	"""Pivot total quantity and sales by region and product."""
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
	pivot = pd.pivot_table(
		sales_df,
		index=[region_column, product_column],
		values=[quantity_column, "sales"],
		aggfunc="sum",
		fill_value=0,
	)
	show_pivot_table(pivot)


def total_quantity_and_sales_by_customer_type(sales_df):
	"""Pivot total quantity and sales by order and customer type."""
	customer_column = get_column(sales_df, "customer_type")
	order_column = get_column(sales_df, "order_type")
	quantity_column = get_column(sales_df, "quantity")
	if customer_column is None or order_column is None or quantity_column is None or "sales" not in sales_df.columns:
		print("Cannot run this analysis; order_type, customer_type, quantity, and sales are required.")
		return
	pivot = pd.pivot_table(
		sales_df,
		index=[order_column, customer_column],
		values=[quantity_column, "sales"],
		aggfunc="sum",
		fill_value=0,
	)
	show_pivot_table(pivot)


def max_min_sales_price_by_category(sales_df):
	"""Pivot minimum and maximum sales price by category."""
	category_column = get_column(sales_df, "product_category")
	price_column = get_column(sales_df, "unit_price")
	if category_column is None or price_column is None:
		print("Cannot run this analysis; product_category and unit_price are required.")
		return
	pivot = pd.pivot_table(
		sales_df,
		index=category_column,
		values=price_column,
		aggfunc=["min", "max"],
		fill_value=0,
	)
	pivot.columns = [f"{statistic}_{field}" for statistic, field in pivot.columns]
	show_pivot_table(pivot)


def unique_employees_by_region(sales_df):
	"""Pivot the unique employee count by region."""
	region_column = get_column(sales_df, "sales_region")
	employee_column = get_column(sales_df, "employee_id")
	if region_column is None or employee_column is None:
		print("Cannot run this analysis; sales_region and employee_id are required.")
		return
	pivot = pd.pivot_table(
		sales_df,
		index=region_column,
		values=employee_column,
		aggfunc="nunique",
		fill_value=0,
	)
	pivot = pivot.rename(columns={employee_column: "unique_employees"})
	show_pivot_table(pivot)


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


MENU_ITEMS = (
	("Show the first n rows of sales data", first_rows),
	("Total sales by region and order_type", total_sales_by_region_order_type),
	("Average sales by region, state, and order type", average_sales_by_region_state_type),
	("Sales by customer type and order type by state", sales_by_customer_type_order_type_state),
	("Total sales quantity and price by region and product", total_quantity_and_sales_by_region_product),
	("Total sales quantity and price by order and customer type", total_quantity_and_sales_by_customer_type),
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
