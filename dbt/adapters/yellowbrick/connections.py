from dbt.adapters.events.logging import AdapterLogger
from dbt.adapters.postgres.connections import PostgresCredentials, PostgresConnectionManager
from dataclasses import dataclass
from typing import Optional, Union
import psycopg2
from dbt_common.events.functions import warn_or_error
from dbt.adapters.events.types import TypeCodeNotFound

logger = AdapterLogger("Yellowbrick")

@dataclass
class YellowbrickCredentials(PostgresCredentials):
    """
    Defines database specific credentials that get added to
    profiles.yml to connect to new adapter
    """

    @property
    def type(self):
        return "yellowbrick"


class YellowbrickConnectionManager(PostgresConnectionManager):
    TYPE = 'yellowbrick'
