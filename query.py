"""
FlowPipe — SQL Query Layer
Run this after pipeline.py to interrogate the database.
"""

import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), "flowpipe_output.db")


def run(sql, label=""):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    if label:
        print(f"\n{'-'*50}")
        print(f"  {label}")
        print(f"{'-'*50}")

    if not rows:
        print("  (no results)")
        return

    headers = rows[0].keys()
    col_w = [max(len(h), max(len(str(r[h])) for r in rows)) for h in headers]

    header_line = "  " + "  ".join(h.upper().ljust(col_w[i]) for i, h in enumerate(headers))
    print(header_line)
    print("  " + "  ".join("-" * w for w in col_w))

    for row in rows:
        print("  " + "  ".join(str(row[h]).ljust(col_w[i]) for i, h in enumerate(headers)))


# ── QUERY 1 ─────────────────────────────────────────────────────────────────
run("""
    SELECT vendor, item, quantity, total_cost, status, department
    FROM orders
    ORDER BY CAST(total_cost AS REAL) DESC
""", "ALL ORDERS — sorted by total cost (highest first)")

# ── QUERY 2 ─────────────────────────────────────────────────────────────────
run("""
    SELECT department,
           COUNT(*)                                      AS order_count,
           SUM(CAST(total_cost AS REAL))                 AS total_spend,
           AVG(CAST(total_cost AS REAL))                 AS avg_order_value
    FROM orders
    GROUP BY department
    ORDER BY total_spend DESC
""", "SPEND BY DEPARTMENT — who is spending the most?")

# ── QUERY 3 ─────────────────────────────────────────────────────────────────
run("""
    SELECT order_id, vendor, item, quantity, total_cost
    FROM orders
    WHERE status = 'needs_approval'
    ORDER BY CAST(total_cost AS REAL) DESC
""", "FLAGGED ORDERS — needs approval before processing")

# ── QUERY 4 ─────────────────────────────────────────────────────────────────
run("""
    SELECT vendor,
           COUNT(*)                        AS num_orders,
           SUM(CAST(total_cost AS REAL))   AS total_spend
    FROM orders
    GROUP BY vendor
    ORDER BY total_spend DESC
""", "VENDOR BREAKDOWN — total spend per supplier")

# ── QUERY 5 ─────────────────────────────────────────────────────────────────
run("""
    SELECT SUM(CAST(total_cost AS REAL))  AS grand_total,
           COUNT(*)                        AS total_orders,
           MAX(CAST(total_cost AS REAL))   AS largest_order,
           MIN(CAST(total_cost AS REAL))   AS smallest_order
    FROM orders
""", "SUMMARY — the full picture in one row")

print()
