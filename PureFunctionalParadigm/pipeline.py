import csv
import json
import sys
from utils import parse_date, safe_float, stats_summary

sys.setrecursionlimit(5000)


def load_csv(path):
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(map(dict, reader))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    def find_list_key(keys):
        if not keys:
            return [data]

        head, *tail = keys
        if isinstance(data, dict) and head in data and isinstance(data[head], list):
            return data[head]

        return find_list_key(tail)

    if isinstance(data, dict):
        return find_list_key(["data", "items", "rows"])
    return data


def recursive_map(func, lst, acc=None):

    if acc is None:
        acc = []

    if not lst:
        return acc

    head, *tail = lst
    processed_val = func(head)
    return recursive_map(func, tail, acc + [processed_val])


def recursive_filter(condition_fn, lst, acc=None):
    if acc is None:
        acc = []

    if not lst:
        return acc

    head, *tail = lst
    if condition_fn(head):
        new_acc = acc + [head]
    else:
        new_acc = acc

    return recursive_filter(condition_fn, tail, new_acc)


def recursive_dict_map(fn, items, acc=None):
    if acc is None:
        acc = {}

    if not items:
        return acc

    (k, v), *tail = items
    new_acc = {**acc, k: fn(k, v)}

    return recursive_dict_map(fn, tail, new_acc)


def handle_missing(rows, fill_values=None):
    fill_values = fill_values or {}

    def fill_row(r):

        def transform(k, v):
            return v if v not in [None, ""] else fill_values.get(k, v)

        return recursive_dict_map(transform, list(r.items()))

    return recursive_map(fill_row, rows)


def standardize_dates(rows, date_fields):

    def standardize_row(r):

        def transform(k, v):
            if k in date_fields:
                return parse_date(v)
            return v

        return recursive_dict_map(transform, list(r.items()))

    return recursive_map(standardize_row, rows)


def standardize_numbers(rows, numeric_fields, precision=2):

    def standardize_row(r):

        def transform(k, v):
            if k in numeric_fields:
                return round(safe_float(v), precision)
            return v

        return recursive_dict_map(transform, list(r.items()))

    return recursive_map(standardize_row, rows)


def filter_rows(rows, condition_fn):
    return recursive_filter(condition_fn, rows)


def compute_sales_growth(rows, current_column="Sales", previous_column="PreviousSales", new_column="SalesGrowth"):
    def compute_row(r):
        cur = safe_float(r.get(current_column, 0))
        prev = safe_float(r.get(previous_column, 0))
        new_val = round((cur - prev) / prev, 4) if prev != 0 else 0.0
        return {**r, new_column: new_val}

    return recursive_map(compute_row, rows)


def aggregate_sum_by_key(rows, key_field, sum_field):

    def aggregate_recursive(lst, accumulator):
        if not lst:
            return accumulator

        head, *tail = lst
        key = head.get(key_field, "UNKNOWN")
        val = safe_float(head.get(sum_field, 0))

        current_sum = accumulator.get(key, 0.0)
        new_acc = accumulator.copy()
        new_acc[key] = current_sum + val

        return aggregate_recursive(tail, new_acc)

    raw_sums = aggregate_recursive(rows, {})

    def format_output(item):
        k, v = item
        return {"key": k, sum_field: round(v, 2)}

    return recursive_map(format_output, list(raw_sums.items()))


def numeric_column_list(rows, column):
    def get_val(r):
        return safe_float(r.get(column))

    def is_valid(r):
        return r.get(column) not in [None, ""]

    valid_rows = recursive_filter(is_valid, rows)
    return recursive_map(get_val, valid_rows)


def analyze_statistics(rows, numeric_columns):

    def analyze_cols_recursive(cols, acc):
        if not cols:
            return acc

        head_col, *tail_cols = cols
        vals = numeric_column_list(rows, head_col)

        new_acc = acc.copy()
        new_acc[head_col] = stats_summary(vals)

        return analyze_cols_recursive(tail_cols, new_acc)

    return analyze_cols_recursive(numeric_columns, {})