from airflow.operators.python import PythonOperator

from .utility import fail, pass_, skip

__all__ = (
    "SkipTask",
    "FailTask",
    "PassTask",
)


def SkipTask(task_id: str, **kwargs) -> PythonOperator:
    return PythonOperator(task_id=task_id, python_callable=skip, **kwargs)


def FailTask(task_id: str, **kwargs) -> PythonOperator:
    return PythonOperator(task_id=task_id, python_callable=fail, **kwargs)


def PassTask(task_id: str, **kwargs) -> PythonOperator:
    return PythonOperator(task_id=task_id, python_callable=pass_, **kwargs)
