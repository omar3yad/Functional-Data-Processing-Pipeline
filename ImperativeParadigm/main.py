# main.py
import os
from pipeline import (
    load_csv, load_json, handle_missing, standardize_dates, standardize_numbers,
    filter_rows, compute_sales_growth, aggregate_sum_by_key,
    analyze_statistics, save_clean_data, save_analysis_summary
)

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
        strategy="fill",
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

    high_sales_rows = filter_rows(standardized_numbers_rows, lambda r: float(r.get("Sales", 0)) > 1000)
    sales_growth_rows = compute_sales_growth(high_sales_rows, current_column="Sales", previous_column="PreviousSales",
                                             new_column="SalesGrowth")

    agg = aggregate_sum_by_key(sales_growth_rows, key_field="Region", sum_field="Sales")
    stats = analyze_statistics(sales_growth_rows, numeric_columns=["Sales", "SalesGrowth"])

    clean_out = os.path.join(OUTPUT_DIR, "clean_data.csv")
    save_clean_data(sales_growth_rows, clean_out)
    print(f"Saved cleaned data to {clean_out}")

    agg_out = os.path.join(OUTPUT_DIR, "agg_by_region.csv")
    if agg:
        from utils import write_csv
        write_csv(agg_out, fieldnames=list(agg[0].keys()), rows=agg)
        print(f"Saved aggregation to {agg_out}")

    summary_out = os.path.join(OUTPUT_DIR, "analysis_summary.txt")
    save_analysis_summary(stats, summary_out)
    print(f"Saved analysis summary to {summary_out}")


if __name__ == "__main__":
    main()
