"""
Mini Data Processing System
----------------------------
Reads a CSV dataset into an array (list) of records, deduplicates records
using content hashing + a hash set, groups/aggregates data using hash maps
(dict), ranks results using array sorting, and prints/exports insights.

Usage:
    python main.py data/transactions.csv
"""

import csv
import hashlib
import json
import sys
from pathlib import Path


def load_dataset(path: str) -> list[dict]:
    """Load CSV into an array (list) of record dicts."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def record_hash(record: dict) -> str:
    """Hash a record's contents to detect exact duplicates."""
    canonical = json.dumps(record, sort_keys=True)
    return hashlib.md5(canonical.encode("utf-8")).hexdigest()


def deduplicate(records: list[dict]) -> tuple[list[dict], int]:
    """
    Remove exact-duplicate records using a hash set (O(1) membership check
    per record instead of O(n) list scanning).
    """
    seen_hashes: set[str] = set()
    cleaned: list[dict] = []
    duplicates = 0

    for record in records:
        h = record_hash(record)
        if h in seen_hashes:
            duplicates += 1
            continue
        seen_hashes.add(h)
        cleaned.append(record)

    return cleaned, duplicates


def group_by_category(records: list[dict]) -> dict[str, list[float]]:
    """Hash map: category -> array of amounts."""
    groups: dict[str, list[float]] = {}
    for record in records:
        category = record["category"]
        amount = float(record["amount"])
        groups.setdefault(category, []).append(amount)
    return groups


def group_by_customer(records: list[dict]) -> dict[str, float]:
    """Hash map: customer_id -> total spend."""
    totals: dict[str, float] = {}
    for record in records:
        cust = record["customer_id"]
        amount = float(record["amount"])
        totals[cust] = totals.get(cust, 0.0) + amount
    return totals


def generate_insights(records: list[dict], duplicates_removed: int) -> dict:
    category_groups = group_by_category(records)
    customer_totals = group_by_customer(records)

    category_summary = {
        category: {
            "count": len(amounts),
            "total": round(sum(amounts), 2),
            "average": round(sum(amounts) / len(amounts), 2),
        }
        for category, amounts in category_groups.items()
    }

    # Array sort for ranking (top categories by total spend)
    top_categories = sorted(
        category_summary.items(), key=lambda kv: kv[1]["total"], reverse=True
    )

    # Array sort for ranking (top customers by total spend)
    top_customers = sorted(
        customer_totals.items(), key=lambda kv: kv[1], reverse=True
    )

    all_amounts = [float(r["amount"]) for r in records]

    return {
        "total_records_after_cleaning": len(records),
        "duplicates_removed": duplicates_removed,
        "overall": {
            "total_revenue": round(sum(all_amounts), 2),
            "average_transaction": round(sum(all_amounts) / len(all_amounts), 2),
            "min_transaction": min(all_amounts),
            "max_transaction": max(all_amounts),
        },
        "category_summary": category_summary,
        "top_categories_by_revenue": [
            {"category": c, "total": v["total"]} for c, v in top_categories
        ],
        "top_customers_by_spend": [
            {"customer_id": c, "total": round(v, 2)} for c, v in top_customers[:3]
        ],
    }


def print_report(insights: dict) -> None:
    print("=== Mini Data Processing System: Insights Report ===\n")
    print(f"Records after cleaning : {insights['total_records_after_cleaning']}")
    print(f"Duplicates removed     : {insights['duplicates_removed']}\n")

    overall = insights["overall"]
    print("Overall stats:")
    print(f"  Total revenue       : {overall['total_revenue']}")
    print(f"  Average transaction : {overall['average_transaction']}")
    print(f"  Min / Max           : {overall['min_transaction']} / {overall['max_transaction']}\n")

    print("Category breakdown:")
    for cat, stats in insights["category_summary"].items():
        print(f"  {cat:<12} count={stats['count']:<3} total={stats['total']:<10} avg={stats['average']}")

    print("\nTop categories by revenue:")
    for entry in insights["top_categories_by_revenue"]:
        print(f"  {entry['category']:<12} {entry['total']}")

    print("\nTop 3 customers by spend:")
    for entry in insights["top_customers_by_spend"]:
        print(f"  {entry['customer_id']:<8} {entry['total']}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_csv>")
        sys.exit(1)

    path = sys.argv[1]
    if not Path(path).exists():
        print(f"File not found: {path}")
        sys.exit(1)

    raw_records = load_dataset(path)
    cleaned_records, duplicates_removed = deduplicate(raw_records)
    insights = generate_insights(cleaned_records, duplicates_removed)

    print_report(insights)

    out_path = Path("insights.json")
    out_path.write_text(json.dumps(insights, indent=2))
    print(f"\nFull insights written to {out_path.resolve()}")


if __name__ == "__main__":
    main()