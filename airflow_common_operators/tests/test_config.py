from airflow_config import DAG, load_config


class TestConfig:
    def test_cleanup_task(self):
        conf = load_config("config", "config")
        d = DAG(dag_id="test_cleanup", config=conf)
        assert len(d.tasks) == 1

    def test_cleanup_render(self):
        conf = load_config("config", "config")
        assert (
            conf.dags["test_cleanup"].render()
            == """# Generated by airflow-config
from airflow.models import DAG
from airflow_common_operators.tasks.dag_clean import create_cleanup_dag_runs

with DAG(schedule="0 0 * * *", max_active_tasks=1, dag_id="test_cleanup") as dag:
    cleanup_task = create_cleanup_dag_runs(task_id="cleanup_task", dag=dag)
"""
        )
