from dbt.adapters.base import Column

class YellowbrickColumn(Column):
    @property
    def data_type(self):
        # on yellowbrick, convert 'name' to varchar(64)
        if self.dtype.lower() == "name":
            return "varchar(64)"
        return super().data_type