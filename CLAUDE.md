# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`dbt-yellowbrick` is a dbt adapter plugin for Yellowbrick Data Warehouse. It extends the PostgreSQL adapter (`dbt-postgres`) with Yellowbrick-specific features: `DISTRIBUTE`, `CLUSTER`, and `SORT` directives, cross-database query support, and `varchar` type coercion (Yellowbrick does not support the `text` type).

Current version targets dbt-core 1.9.x–1.10.x.

## Common Commands

```bash
# Install for development
pip install -e . -r dev-requirements.txt

# Run functional tests (requires a live Yellowbrick instance)
pytest tests/functional

# Run via tox
tox -e unit
tox -e integration-yellowbrick

# Code quality (format, lint, type-check)
pre-commit run --all-files
mypy dbt/adapters/yellowbrick/
flake8 dbt/adapters/yellowbrick/

# Build distribution
python setup.py sdist bdist_wheel
```

Functional tests read credentials from environment variables: `DBT_TEST_YB_HOST`, `DBT_TEST_YB_PORT`, `DBT_TEST_YB_USER`, `DBT_TEST_YB_PASS`, `DBT_TEST_YB_DBNAME`. A `test.env` file (not committed) can supply these via `pytest-dotenv`.

## Architecture

The adapter is split into two parts:

### Python layer (`dbt/adapters/yellowbrick/`)
- **`connections.py`** — `YellowbrickCredentials` and `YellowbrickConnectionManager`, both thin subclasses of their Postgres equivalents. TYPE = `"yellowbrick"`.
- **`impl.py`** — `YellowbrickAdapter` extends `PostgresAdapter`.
  - `verify_database()` is overridden to allow cross-database references (disabled in Postgres).
  - `_get_catalog_schemas()` supports multiple databases.
  - `valid_incremental_strategies()` returns `["append", "delete+insert"]` (no `merge`).
  - `convert_text_type()` maps `text` → `varchar`.
- **`relation.py`** — Max identifier length is 127 (Yellowbrick limit is 128); quoting is disabled for all parts.
- **`column.py`** — Maps the Postgres `name` type to `varchar(64)`.
- **`__init__.py`** — Registers the plugin with `dependencies=['postgres']`.

### SQL/Jinja layer (`dbt/include/yellowbrick/macros/`)
- **`adapters.sql`** — Overrides `yellowbrick__create_table_as` to append `DISTRIBUTE`, `CLUSTER ON`, and `SORT ON` clauses. Handles contract enforcement (column constraints). All other adapter macros delegate to Postgres equivalents.
- **`materializations/distribute.sql`** — Generates `DISTRIBUTE ON (col)`, `DISTRIBUTE REPLICATE`, or `DISTRIBUTE RANDOM`.
- **`materializations/cluster.sql`** — Generates `CLUSTER ON (col1, col2, ...)` (up to 4 columns).
- **`materializations/sort.sql`** — Generates `SORT ON (col1, ...)`.
- **`catalog.sql`** — Catalog introspection queries.
- **`utils/hash.sql`** — Uses Yellowbrick's native `HASH()` function.

### Plugin registration flow
`__init__.py` → `AdapterPlugin(adapter=YellowbrickAdapter, credentials=YellowbrickCredentials, include_path=..., dependencies=['postgres'])`

When dbt resolves macros, it searches Yellowbrick macros first, then falls back to the `postgres` dependency, then dbt-core defaults.

## Code Style
- Black with line length 99, targeting Python 3.8+.
- Flake8 for linting, mypy for type checks (pre-commit enforces all three).
