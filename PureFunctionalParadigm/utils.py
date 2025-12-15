from datetime import datetime
import csv
import statistics
import sys

sys.setrecursionlimit(5000)


def parse_date(date_str):

    if date_str is None or date_str == "":
        return "UNKNOWN"

    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]

    def try_parse_recursive(fmt_list):

        if not fmt_list:
            return date_str

        current_fmt, *remaining_fmts = fmt_list
        try:
            dt = datetime.strptime(date_str.strip(), current_fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return try_parse_recursive(remaining_fmts)

    return try_parse_recursive(formats)


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def stats_summary(values):

    def recursive_clean(lst, acc=None):
        if acc is None:
            acc = []
        if not lst:
            return acc

        head, *tail = lst
        if head is not None:
            new_acc = acc + [head]
        else:
            new_acc = acc
        return recursive_clean(tail, new_acc)

    clean_values = recursive_clean(values)

    if not clean_values:
        return {"count": 0}

    return {
        "count": len(clean_values),
        "mean": statistics.mean(clean_values),
        "median": statistics.median(clean_values),
        "variance": statistics.pvariance(clean_values) if len(clean_values) > 1 else 0.0,
        "min": min(clean_values),
        "max": max(clean_values)
    }


def write_csv(path, fieldnames, rows):

    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        def write_rows_recursive(row_list):
            if not row_list:
                return

            head, *tail = row_list
            writer.writerow(head)  # Side Effect
            write_rows_recursive(tail)

        write_rows_recursive(rows)