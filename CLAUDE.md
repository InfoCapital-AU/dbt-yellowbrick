# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`dbt-yellowbrick` is a dbt adapter plugin for Yellowbrick Data Warehouse. It extends the PostgreSQL adapter (`dbt-postgres`) with Yellowbrick-specific features: `DISTRIBUTE`, `CLUSTER`, and `SORT` directives, cross-database query support, and `varchar` type coercion (Yellowbrick does not support the `text` type).

Current version targets dbt-core 1.12.x (dbt-postgres 1.11.x, dbt-adapters ≥1.24.5). Requires Python 3.10+.

## Common Commands

```bash
# Install for development
# NOTE: this repo still uses the legacy pkgutil-style namespace packages
# (dbt/__init__.py + dbt/adapters/__init__.py use pkgutil.extend_path) for
# the dbt/dbt.adapters/dbt.include namespaces. Modern setuptools PEP 660
# editable installs are incompatible with that scheme and will fail to
# register the adapter (`dbt --version` / `dbt parse` report
# "Could not find adapter type yellowbrick!"). Force the legacy
# (PEP 660 "compat") editable mode instead:
pip install -e . -r dev-requirements.txt --config-settings editable_mode=compat

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
- **`relation.py`** — Extends `PostgresRelation` (not `BaseRelation` directly, so it keeps `renameable_relations`/`replaceable_relations` and materialized-view config diffing). Max identifier length is 127 (Yellowbrick limit is 128); quoting is disabled for all parts.
- **`column.py`** — Extends `PostgresColumn` (keeps its unbounded-`character varying` handling) and additionally maps the Postgres `name` type to `varchar(64)`.
- **`__init__.py`** — Registers the plugin with `dependencies=['postgres']`.

### SQL/Jinja layer (`dbt/include/yellowbrick/macros/`)
- **`adapters.sql`** — Overrides `yellowbrick__create_table_as` to append `DISTRIBUTE`, `CLUSTER ON`, and `SORT ON` clauses. Handles contract enforcement (column constraints). Also overrides `yellowbrick__alter_column_type` (used by `on_schema_change: sync_all_columns` and `adapter.expand_target_column_types`, the latter called on every non-full-refresh incremental run): Yellowbrick supports neither `ALTER COLUMN ... TYPE ...` ("SET DATA TYPE is not supported") nor `ALTER TABLE ... DROP COLUMN` ("DROP COLUMN is not supported"), so dbt-core's generic `default__alter_column_type` (add/copy/drop/rename) fails outright — the override instead rebuilds the table with the new column type and swaps it into place via `RENAME`. All other adapter macros delegate to Postgres equivalents.
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
