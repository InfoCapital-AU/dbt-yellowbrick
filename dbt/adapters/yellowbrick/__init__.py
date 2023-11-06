from dbt.adapters.yellowbrick.connections import YellowbrickConnectionManager # noqa
from dbt.adapters.yellowbrick.connections import YellowbrickCredentials
from dbt.adapters.yellowbrick.impl import YellowbrickAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import yellowbrick


Plugin = AdapterPlugin(
    adapter=YellowbrickAdapter,
    credentials=YellowbrickCredentials,
    include_path=yellowbrick.PACKAGE_PATH,
    dependencies=['postgres']
)
