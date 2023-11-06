from dbt.adapters.yellowbrick import YellowbrickConnectionManager
from dbt.adapters.postgres.impl import PostgresAdapter
from dbt.events import AdapterLogger
from dbt.adapters.base.meta import available

from dbt.exceptions import (
    CrossDbReferenceProhibitedError,
    IndexConfigNotDictError,
    IndexConfigError,
    DbtRuntimeError,
    UnexpectedDbReferenceError,
    CompilationError
)

logger = AdapterLogger("Yellowbrick")

class YellowbrickAdapter(PostgresAdapter):
    ConnectionManager = YellowbrickConnectionManager

    # Override to allow cross-database queries which are supported in Yellowbrick
    # Source: https://github.com/dbt-labs/dbt-core/blob/7317de23a3199fe2f9bb212406dc523f134e7bfb/plugins/postgres/dbt/adapters/postgres/impl.py#L121C1-L128C1    

    @available
    def verify_database(self, database):
        if database.startswith('"'):
            database = database.strip('"')
        expected = self.config.credentials.database

        # Yelowbrick supports Cross-db
        allow_multiple_databases = True

        if database.lower() != expected.lower() and not allow_multiple_databases:
            raise NotImplementedError(
                "Cross-db references allowed only in Yellowbrick. ({} vs {})".format(database, expected)
            )
        # return an empty string on success so macros can call this
        return ""

    def _get_catalog_schemas(self, manifest):
        # redshift(besides ra3) only allow one database (the main one)
        schemas = super(PostgresAdapter, self)._get_catalog_schemas(manifest)
        try:
            return schemas.flatten(allow_multiple_databases=True)
        except DbtRuntimeError as exc:
            msg = f"Cross-db references allowed in {self.type()} Yellowbrick. Got {exc.msg}"
            raise CompilationError(msg)

    def valid_incremental_strategies(self):
        return ["append", "delete+insert"]