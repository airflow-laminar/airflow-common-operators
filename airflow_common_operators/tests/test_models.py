from unittest.mock import MagicMock

from airflow_common_operators.models import DagCleanup


class TestModels:
    def test_dag_cleanup(self):
        d = DagCleanup()
        d.cleanup_dag_runs(session=MagicMock(), params={})
