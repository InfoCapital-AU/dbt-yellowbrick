from dbt.events import AdapterLogger
from dbt.adapters.postgres.connections import PostgresCredentials, PostgresConnectionManager

logger = AdapterLogger("Yellowbrick")


class YellowbrickCredentials(PostgresCredentials):

    @property
    def type(self):
        return "yellowbrick"


class YellowbrickConnectionManager(PostgresConnectionManager):
    TYPE = 'yellowbrick'