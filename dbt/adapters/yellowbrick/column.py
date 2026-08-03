from dbt.adapters.postgres.column import PostgresColumn


class YellowbrickColumn(PostgresColumn):
    @property
    def data_type(self):
        # on yellowbrick, convert 'name' to varchar(64)
        if self.dtype.lower() == "name":
            return "varchar(64)"
        return super().data_type
