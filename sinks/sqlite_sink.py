import sqlite3


def write(rows, db_path, table="orders"):
    """Write a list of row dicts into a SQLite database table."""
    if not rows:
        print("  [sink] No rows to write.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # build the table from whatever columns the data has
    columns = list(rows[0].keys())
    col_defs = ", ".join(f'"{c}" TEXT' for c in columns)
    cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({col_defs})')

    # insert every row
    placeholders = ", ".join("?" for _ in columns)
    for row in rows:
        values = [str(row.get(c, "")) for c in columns]
        cursor.execute(f'INSERT INTO "{table}" VALUES ({placeholders})', values)

    conn.commit()
    conn.close()
    print(f"  [sink] Wrote {len(rows)} rows -> {db_path} (table: {table})")
