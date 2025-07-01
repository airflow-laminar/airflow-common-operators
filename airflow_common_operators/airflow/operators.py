from airflow_pydantic.airflow import PythonOperator

from .utility import fail, pass_, skip

__all__ = (
    "Skip",
    "Fail",
    "Pass",
)


def Skip(task_id: str, **kwargs) -> PythonOperator:
    return PythonOperator(task_id=task_id, python_callable=skip, **kwargs)


def Fail(task_id: str, **kwargs) -> PythonOperator:
    return PythonOperator(task_id=task_id, python_callable=fail, **kwargs)


def Pass(task_id: str, **kwargs) -> PythonOperator:
    return PythonOperator(task_id=task_id, python_callable=pass_, **kwargs)
