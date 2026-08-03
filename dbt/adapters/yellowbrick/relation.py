from dataclasses import dataclass, field

from dbt.adapters.base.relation import Policy
from dbt.adapters.postgres.relation import PostgresRelation

MAX_CHARACTERS_IN_IDENTIFIER = 127


@dataclass
class YellowbrickQuotePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = False


@dataclass(frozen=True, eq=False, repr=False)
class YellowbrickRelation(PostgresRelation):
    quote_policy: Policy = field(default_factory=lambda: YellowbrickQuotePolicy())

    def relation_max_name_length(self):
        # Max table name length in Yellowbrick is 128 (https://docs.yellowbrick.com/6.7.1/ybd_sqlref/create_table.html)
        return MAX_CHARACTERS_IN_IDENTIFIER
