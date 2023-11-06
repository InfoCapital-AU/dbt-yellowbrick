from dataclasses import dataclass, field

from dbt.adapters.base.relation import BaseRelation, Policy
from dbt.exceptions import DbtRuntimeError


@dataclass
class YellowbrickQuotePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = False


@dataclass(frozen=True, eq=False, repr=False)
class YellowbrickRelation(BaseRelation):
    quote_policy: Policy = field(default_factory=lambda: YellowbrickQuotePolicy())

    def __post_init__(self):
        # Check for length of Yellowbrick table/view names.
        # Check self.type to exclude test relation identifiers
        if (
            self.identifier is not None
            and self.type is not None
            and len(self.identifier) > self.relation_max_name_length()
        ):
            raise DbtRuntimeError(
                f"Relation name '{self.identifier}' "
                f"is longer than {self.relation_max_name_length()} characters"
            )

    def relation_max_name_length(self):
        # Max table name length in Yellowbrick is 128 (https://docs.yellowbrick.com/6.7.1/ybd_sqlref/create_table.html)
        return 128