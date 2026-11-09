"""Interactive sales pivot generator with Excel export support."""

import re
import sys
import time
from pathlib import Path
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


def export_to_excel(result, sheet_name):
	"""Ask whether to export a result and write it to an Excel workbook."""
	while True:
		choice = input("Export these results to an Excel file? (y/n): ").strip().lower()
		if choice in {"n", "no"}:
			return
		if choice in {"y", "yes"}:
			break
		print("Enter y or n.")

	while True:
		filename = input("Filename for the Excel file: ").strip()
		if filename:
			break
		print("Filename cannot be blank.")

	output_path = Path(filename).expanduser()
	if output_path.suffix.lower() != ".xlsx":
		output_path = output_path.with_suffix(".xlsx")
	try:
		result.to_excel(output_path, sheet_name=sheet_name[:31])
	except (ImportError, OSError, ValueError) as error:
		print(f"Could not export the results: {error}")
		return
	print(f"Results exported to {output_path}.")


def display_and_export(result, title, sheet_name):
	"""Display one pivot result, then offer to save it as an Excel file."""
	if result.empty:
		print("No data is available for this result.")
		return
	print(f"\n{title}")
	print(result.to_string(index=False) if isinstance(result.index, pd.RangeIndex) else result.to_string())
	export_to_excel(result, sheet_name)


def pivot_table_generator(data):
	"""Collect dimensions, measures, and aggregations, then print and export results."""
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

	display_and_export(pivot, "Custom pivot table:", "Pivot Results")
	return pivot


def sales_by_region_product(data):
	"""Show quantity and sales by region/product with each product's regional share."""
	region_column = get_column(data, "sales_region")
	product_column = None
	for field in ("produce_name", "product_name", "product_number", "product_category"):
		product_column = get_column(data, field)
		if product_column is not None:
			break
	quantity_column = get_column(data, "quantity")
	sale_price_column = get_column(data, "sale_price")
	if None in (region_column, product_column, quantity_column, sale_price_column):
		print(
			"Cannot run this analysis; sales_region, product name/category, quantity, "
			"and sale_price are required."
		)
		return None
	assert region_column is not None
	assert product_column is not None
	assert quantity_column is not None
	assert sale_price_column is not None
	assert region_column is not None
	assert product_column is not None
	assert quantity_column is not None
	assert sale_price_column is not None

	pivot = pd.pivot_table(
		data,
		index=[region_column, product_column],
		values=[quantity_column, sale_price_column],
		aggfunc="sum",
		fill_value=0,
	).reset_index()
	region_quantity_totals = pivot.groupby(region_column)[quantity_column].transform("sum")
	region_sales_totals = pivot.groupby(region_column)[sale_price_column].transform("sum")
	pivot["quantity_percentage"] = 0.0
	pivot["sales_percentage"] = 0.0
	nonzero_quantity = region_quantity_totals != 0
	nonzero_sales = region_sales_totals != 0
	pivot.loc[nonzero_quantity, "quantity_percentage"] = (
		pivot.loc[nonzero_quantity, quantity_column]
		.div(region_quantity_totals[nonzero_quantity])
		.mul(100)
		.round(2)
	)
	pivot.loc[nonzero_sales, "sales_percentage"] = (
		pivot.loc[nonzero_sales, sale_price_column]
		.div(region_sales_totals[nonzero_sales])
		.mul(100)
		.round(2)
	)
	display_and_export(pivot, "Sales by region and product with regional percentages:", "Region Product")
	return pivot


def exit_program(_data):
	"""Signal that the interactive menu should exit."""
	print("Goodbye.")
	return False


MENU_ITEMS = (
	("Create a custom pivot table", pivot_table_generator),
	("Sales by region and product with percentages", sales_by_region_product),
	("Exit", exit_program),
)


def run_menu(data):
	"""Run the pivot-generator menu until the user chooses Exit."""
	while True:
		print("\n--- Sales Pivot Table Generator ---")
		for number, (label, _function) in enumerate(MENU_ITEMS, start=1):
			print(f"{number}. {label}")
		try:
			selection = int(input("Select an option: "))
		except ValueError:
			print("Enter the number of a menu option.")
			continue
		if not 1 <= selection <= len(MENU_ITEMS):
			print(f"Choose a number from 1 to {len(MENU_ITEMS)}.")
			continue
		if MENU_ITEMS[selection - 1][1](data) is False:
			break


if __name__ == "__main__":
	sales_data = load_sales_data()
	run_menu(sales_data)
