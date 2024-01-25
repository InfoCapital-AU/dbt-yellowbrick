import pytest

from dbt.tests.adapter.basic.test_base import BaseSimpleMaterializations
from dbt.tests.adapter.basic.test_singular_tests import BaseSingularTests
from dbt.tests.adapter.basic.test_singular_tests_ephemeral import (
    BaseSingularTestsEphemeral
)
from dbt.tests.adapter.basic.test_empty import BaseEmpty
from dbt.tests.adapter.basic.test_ephemeral import BaseEphemeral
from dbt.tests.adapter.basic.test_incremental import BaseIncremental
from dbt.tests.adapter.basic.test_generic_tests import BaseGenericTests
from dbt.tests.adapter.basic.test_snapshot_check_cols import BaseSnapshotCheckCols
from dbt.tests.adapter.basic.test_snapshot_timestamp import BaseSnapshotTimestamp
from dbt.tests.adapter.basic.test_adapter_methods import BaseAdapterMethod


class TestSimpleMaterializationsYellowbrick(BaseSimpleMaterializations):
    pass


class TestSingularTestsYellowbrick(BaseSingularTests):
    pass


class TestSingularTestsEphemeralYellowbrick(BaseSingularTestsEphemeral):
    pass


class TestEmptyYellowbrick(BaseEmpty):
    pass


class TestEphemeralYellowbrick(BaseEphemeral):
    pass


class TestIncrementalYellowbrick(BaseIncremental):
    pass


class TestGenericTestsYellowbrick(BaseGenericTests):
    pass


class TestSnapshotCheckColsYellowbrick(BaseSnapshotCheckCols):
    pass


class TestSnapshotTimestampYellowbrick(BaseSnapshotTimestamp):
    pass


class TestBaseAdapterMethodYellowbrick(BaseAdapterMethod):
    pass
