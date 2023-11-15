from dataclasses import dataclass, field

from dbt.adapters.base.relation import BaseRelation, Policy


@dataclass
class YellowbrickQuotePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = False


@dataclass(frozen=True, eq=False, repr=False)
class YellowbrickRelation(BaseRelation):
    quote_policy: Policy = field(default_factory=lambda: YellowbrickQuotePolicy())