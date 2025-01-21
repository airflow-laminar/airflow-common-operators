from typing import List, Optional

from airflow.models.baseoperator import BaseOperator
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

from .common import fail, pass_

__all__ = ("all_success_any_failure",)


def all_success_any_failure(
    *,
    task_id: str,
    tasks: List[BaseOperator],
    dag: DAG,
    queue: Optional[str] = None,
):
    any_ssh_failure = PythonOperator(
        task_id=f"{task_id}-any-failure",
        python_callable=fail,
        queue=queue,
        trigger_rule="one_failed",
        dag=dag,
    )
    all_ssh_success = PythonOperator(
        task_id=f"{task_id}-all-success",
        python_callable=pass_,
        queue=queue,
        trigger_rule="none_failed",
        dag=dag,
    )

    for task in tasks:
        task >> any_ssh_failure
        task >> all_ssh_success

    return any_ssh_failure, all_ssh_success
