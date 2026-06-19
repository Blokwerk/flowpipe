# FlowPipe

A universal data pipeline framework built in Python. Drop in any data source, define your business rules, and route the output wherever it needs to go.

## The idea

Every business — from aerospace manufacturers to food production to general suppliers — does the same thing with data: something comes in, decisions get made about it, and it goes somewhere. FlowPipe makes that loop reusable across any industry.

```
Source → Rules Engine → Sink
```

## What it does

- **Ingests** CSV files (PDF and API adapters coming next)
- **Applies business rules** — calculates totals, flags large orders, routes by vendor, validates data
- **Writes to a SQLite database** — queryable with standard SQL
- **Reports** — GROUP BY department spend, flag approvals, vendor breakdowns, summaries

## Example output

Run the pipeline against a sample order dataset spanning Boeing, French's Factory, and ACME Corp:

```
order 1004 | Boeing        | qty: 1,200,000 | total: $264,000,000 | needs_approval | aerospace_procurement
order 1002 | French's      | qty: 2,000,000 | total: $40,000       | needs_approval | food_manufacturing
order 1003 | ACME Corp     | qty: 300        | total: $13,500       | pending        | general_supply
```

Then query the database:

```sql
SELECT department, SUM(total_cost) AS total_spend
FROM orders
GROUP BY department
ORDER BY total_spend DESC;
```

## Run it

```bash
python pipeline.py   # ingest + transform + load
python query.py      # SQL reports against the output database
```

No dependencies beyond the Python standard library. SQLite is built in.

## Structure

```
adapters/       CSV reader — plug in new formats here
rules/          Business logic — if/then rules in plain Python
sinks/          Output destinations — SQLite, more coming
sample_data/    Example order data
pipeline.py     Wires everything together
query.py        SQL report layer
```

## Built with

- Python 3
- SQLite (via the built-in `sqlite3` module)
- No third-party dependencies

## Roadmap

- PDF adapter (invoices, contracts)
- REST API adapter
- PostgreSQL sink
- YAML-defined rules (no code required)
- Web dashboard for non-technical users
