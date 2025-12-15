# utils.py
from datetime import datetime
import csv
import statistics


def parse_date(date_str):
    if date_str is None:
        return None
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            continue
    return date_str


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def stats_summary(values):
    clean = []
    for v in values:
        if v is not None:
            clean.append(v)

    if not clean:
        return {"count": 0}

    summary = {
        "count": len(clean),
        "mean": statistics.mean(clean),
        "median": statistics.median(clean),
        "variance": statistics.pvariance(clean) if len(clean) > 1 else 0.0,
        "min": min(clean),
        "max": max(clean)
    }
    return summary

