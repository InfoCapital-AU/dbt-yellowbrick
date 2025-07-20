from dbt.adapters.events.logging import AdapterLogger
from dbt.adapters.postgres.connections import PostgresCredentials, PostgresConnectionManager
from dataclasses import dataclass

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