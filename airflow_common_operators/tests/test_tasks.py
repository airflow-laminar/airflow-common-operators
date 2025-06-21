from airflow import DAG

from airflow_common_operators import DagCleanupTask


class TestModels:
    def test_dag_cleanup(self):
        d = DAG(dag_id="test_dag_cleanup")
        t = DagCleanupTask(dag=d, task_id="test_dag_cleanup_task")
        assert t
