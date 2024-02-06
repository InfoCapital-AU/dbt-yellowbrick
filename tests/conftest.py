import pytest
import os

# import json

# Import the fuctional fixtures as a plugin
# Note: fixtures with session scope need to be local

pytest_plugins = ["dbt.tests.fixtures.project"]


# The profile dictionary, used to write out profiles.yml
@pytest.fixture(scope="class")
def dbt_profile_target():
    return {
        "type": "yellowbrick",
        "threads": 1,
        "host": os.getenv("DBT_TEST_YB_HOST"),
        "port": int(os.getenv("DBT_TEST_YB_PORT")),
        "user": os.getenv("DBT_TEST_YB_USER"),
        "pass": os.getenv("DBT_TEST_YB_PASS"),
        "dbname": os.getenv("DBT_TEST_YB_DBNAME"),
    }
