import os
from pipeline import (
    load_csv, handle_missing, standardize_dates, standardize_numbers,
    filter_rows, compute_sales_growth, aggregate_sum_by_key,
    analyze_statistics
)
from utils import write_csv, safe_float

PROJECT_ROOT = os.path.dirname(__file__)
DATA_DIR = os.path.join(PROJECT_ROOT, "..", "Data")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "..", "Output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    csv_path = os.path.join(DATA_DIR, "input.csv")
    raw_rows = load_csv(csv_path)
    print(f"Loaded {len(raw_rows)} rows")

    filled_rows = handle_missing(
        raw_rows,
        fill_values={
            "Date": "UNKNOWN",
            "Region": "UNKNOWN",
            "Sales": 0.0,
            "PreviousSales": 0.0,
            "Product": "UNKNOWN",
            "SalesGrowth": 0.0
        }
    )

    standardized_dates_rows = standardize_dates(filled_rows, date_fields=["Date"])
    standardized_numbers_rows = standardize_numbers(standardized_dates_rows, numeric_fields=["Sales", "PreviousSales"],
                                               precision=2)
    high_sales_rows = filter_rows(standardized_numbers_rows, lambda r: safe_float(r.get("Sales", 0)) > 1000)
    sales_growth_rows = compute_sales_growth(high_sales_rows, "Sales", "PreviousSales", "SalesGrowth")
    agg = aggregate_sum_by_key(sales_growth_rows, "Region", "Sales")
    stats = analyze_statistics(sales_growth_rows, ["Sales", "SalesGrowth"])

    clean_out = os.path.join(OUTPUT_DIR, "clean_data.csv")
    write_csv(clean_out, fieldnames=list(sales_growth_rows[0].keys()), rows=sales_growth_rows)
    print(f"Saved cleaned data to {clean_out}")

    agg_out = os.path.join(OUTPUT_DIR, "agg_by_region.csv")
    write_csv(agg_out, fieldnames=list(agg[0].keys()), rows=agg)
    print(f"Saved aggregation to {agg_out}")

    summary_out = os.path.join(OUTPUT_DIR, "analysis_summary.txt")

    def write_summary_recursive(file_obj, stats_items):
        if not stats_items:
            return
        col, s = stats_items[0]
        file_obj.write(f"Column: {col}\n")

        def write_details(details_items):
            if not details_items:
                return
            k, v = details_items[0]
            file_obj.write(f"  {k}: {v}\n")
            write_details(details_items[1:])

        write_details(list(s.items()))
        file_obj.write("\n")
        write_summary_recursive(file_obj, stats_items[1:])

    with open(summary_out, "w", encoding="utf-8") as f:
        write_summary_recursive(f, list(stats.items()))

    print(f"Saved analysis summary to {summary_out}")


if __name__ == "__main__":
    main()
