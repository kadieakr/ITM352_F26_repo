"""Interactive sales-data pivot table generator."""

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
	"employee_name",
	"sales_region",
	"product_category",
	"order_type",
	"customer_type",
	"quantity",
	"unit_price",
}

ROW_OPTIONS = (
	("employee_name", "employee_name"),
	("sales_region", "sales_region"),
	("product_category", "product_category"),
)
COLUMN_OPTIONS = (
	("order_type", "order_type"),
	("customer_type", "customer_type"),
)
VALUE_OPTIONS = (
	("quantity", "quantity"),
	("sale_price", "sale_price"),
)
AGGREGATION_OPTIONS = (
	("sum", "sum"),
	("mean", "mean"),
	("count", "count"),
)


def normalize_column_name(column_name):
	"""Normalize column names to match common header styles."""
	return re.sub(r"[^a-z0-9]+", "_", str(column_name).strip().lower()).strip("_")


def get_column(data, requested_name):
	"""Find the actual DataFrame column matching a normalized field name."""
	return next(
		(column for column in data.columns if normalize_column_name(column) == requested_name),
		None,
	)


def load_sales_data():
	"""Load the shared Google Drive CSV, normalize numeric fields, and report status."""
	print("Loading sales_data.csv from Google Drive...", flush=True)
	start_time = time.perf_counter()
	try:
		data = pd.read_csv(SALES_DATA_URL)
	except Exception as error:
		print(
			"Error: Could not load sales_data.csv from Google Drive. "
			"Check your internet connection and confirm the file is shared "
			f"for access. Details: {error}",
			file=sys.stderr,
		)
		raise SystemExit(1) from error

	load_time = time.perf_counter() - start_time
	data = data.fillna(0)
	quantity_column = get_column(data, "quantity")
	unit_price_column = get_column(data, "unit_price")
	if quantity_column is not None:
		data[quantity_column] = pd.to_numeric(data[quantity_column], errors="coerce").fillna(0)
	if unit_price_column is not None:
		data[unit_price_column] = pd.to_numeric(data[unit_price_column], errors="coerce").fillna(0)

	if quantity_column is not None and unit_price_column is not None:
		data["sale_price"] = data[quantity_column] * data[unit_price_column]
	else:
		sales_column = get_column(data, "sales")
		if sales_column is not None:
			data["sale_price"] = pd.to_numeric(data[sales_column], errors="coerce").fillna(0)

	print(f"Successfully loaded sales_data.csv in {load_time:.2f} seconds.")
	print(f"Rows of data: {len(data):,}")
	print("Available columns: " + ", ".join(map(str, data.columns)))
	available_fields = {normalize_column_name(column) for column in data.columns}
	missing_fields = sorted(REQUIRED_FIELDS - available_fields)
	if missing_fields:
		print(
			"Warning: Missing required field(s): "
			f"{', '.join(missing_fields)}. Some pivot-table choices may not work."
		)
	return data


def prompt_for_choices(title, options, allow_empty=False):
	"""Prompt for one or more comma-separated menu numbers."""
	print(f"\n{title}")
	for number, (label, _field) in enumerate(options, start=1):
		print(f"{number}. {label}")
	if allow_empty:
		print("Enter the number(s) of your choice(s), separated by commas (enter for no grouping):")
	else:
		print("Enter the number(s) of your choice(s), separated by commas:")

	while True:
		response = input("Your choice: ").strip()
		if not response and allow_empty:
			return []
		try:
			selections = [int(value.strip()) for value in response.split(",")]
		except ValueError:
			print("Invalid input. Enter menu number(s) separated by commas.")
			continue
		if not selections or any(number < 1 or number > len(options) for number in selections):
			print(f"Choose number(s) from 1 to {len(options)}.")
			continue
		if len(set(selections)) != len(selections):
			print("Do not repeat a menu number.")
			continue
		return [options[number - 1][1] for number in selections]


def pivot_table_generator(data):
	"""Collect dimensions, measures, and aggregations, then print the pivot table."""
	row_fields = prompt_for_choices("Select rows:", ROW_OPTIONS)
	column_fields = prompt_for_choices("Select columns (optional):", COLUMN_OPTIONS, allow_empty=True)
	value_fields = prompt_for_choices("Select values:", VALUE_OPTIONS)
	aggregations = prompt_for_choices("Select aggregation function:", AGGREGATION_OPTIONS)

	actual_rows = [get_column(data, field) for field in row_fields]
	actual_columns = [get_column(data, field) for field in column_fields]
	actual_values = [get_column(data, field) for field in value_fields]
	missing = [
		field
		for field, actual in zip(row_fields + column_fields + value_fields, actual_rows + actual_columns + actual_values)
		if actual is None
	]
	if missing:
		print("Cannot create the pivot table; selected field(s) are missing: " + ", ".join(missing))
		return None

	aggfuncs: list[Literal["sum", "mean", "count"]] = [
		cast(Literal["sum", "mean", "count"], function) for function in aggregations
	]
	aggfunc: Literal["sum", "mean", "count"] | list[Literal["sum", "mean", "count"]]
	aggfunc = aggfuncs[0] if len(aggfuncs) == 1 else aggfuncs
	try:
		pivot = pd.pivot_table(
			data,
			index=actual_rows,
			columns=actual_columns or None,
			values=actual_values,
			aggfunc=aggfunc,
			fill_value=0,
		)
	except (KeyError, TypeError, ValueError) as error:
		print(f"Could not create the pivot table: {error}")
		return None

	if pivot.empty:
		print("No data is available for the selected fields.")
	else:
		print("\nPivot table:")
		print(pivot.to_string())
	return pivot


if __name__ == "__main__":
	sales_data = load_sales_data()
	pivot_table_generator(sales_data)
