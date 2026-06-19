"""
FlowPipe — Universal Data Pipeline Framework
Source → Rules → Sink

Usage:
    python pipeline.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from adapters import csv_adapter
from rules import engine
from sinks import sqlite_sink


def run(source_path, db_path):
    print(f"\n{'='*50}")
    print(f"  FLOWPIPE — starting pipeline")
    print(f"{'='*50}")

    # ── STEP 1: SOURCE ──────────────────────────────
    print(f"\n[source] Reading: {source_path}")
    rows = csv_adapter.read(source_path)
    print(f"[source] Loaded {len(rows)} rows")

    # ── STEP 2: RULES ───────────────────────────────
    print(f"\n[rules]  Applying {len(engine.RULES)} rules...")
    processed = []
    for row in rows:
        result = engine.apply(row)
        processed.append(result)
        flag = result.get("flag", "")
        label = f"  *** {flag}" if flag else ""
        print(f"  order {result['order_id']} | {result['vendor']:<22} | "
              f"qty: {result['quantity']:>10,} | "
              f"total: ${result['total_cost']:>14,.2f} | "
              f"{result['status']:<16} | {result['department']}{label}")

    # ── STEP 3: SINK ────────────────────────────────
    print(f"\n[sink]   Writing to database...")
    sqlite_sink.write(processed, db_path)

    print(f"\n{'='*50}")
    print(f"  PIPELINE COMPLETE")
    print(f"  {len(processed)} records processed")
    needs_approval = [r for r in processed if r.get("flag") == "LARGE_ORDER"]
    print(f"  {len(needs_approval)} orders flagged for approval")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    BASE = os.path.dirname(__file__)
    run(
        source_path=os.path.join(BASE, "sample_data", "orders.csv"),
        db_path=os.path.join(BASE, "flowpipe_output.db"),
    )
