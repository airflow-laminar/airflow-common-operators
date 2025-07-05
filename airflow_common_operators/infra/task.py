from typing import Optional, Type

from airflow_pydantic import CallablePath, Task, TaskArgs
from airflow_pydantic.airflow import PythonOperator
from pydantic import Field, field_validator

__all__ = ("JournalctlClean", "JournalctlCleanOperator", "JournalctlCleanOperatorArgs", "JournalctlCleanTask", "JournalctlCleanTaskArgs")


def clean_journalctl(sudo: Optional[bool] = True, days: Optional[int] = 2):
    days = days or 2
    cmd = f"sudo journalctl --vacuum-time={days}d" if sudo else f"journalctl --vacuum-time={days}d"
    return cmd


class JournalctlClean(PythonOperator):
    def __init__(self, sudo: Optional[bool] = True, days: Optional[int] = 2, **kwargs):
        if "python_callable" in kwargs:
            raise ValueError("JournalctlClean does not accept 'python_callable' as an argument.")
        super().__init__(python_callable=lambda: clean_journalctl(sudo=sudo, days=days), **kwargs)


class JournalctlCleanTaskArgs(TaskArgs):
    sudo: Optional[bool] = Field(default=True)
    days: Optional[int] = Field(default=2)


# Alias
JournalctlCleanOperatorArgs = JournalctlCleanTaskArgs


class JournalctlCleanTask(Task, JournalctlCleanTaskArgs):
    operator: CallablePath = Field(default="airflow_common_operators.JournalctlClean", validate_default=True)

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, v: Type) -> Type:
        if v is not JournalctlClean:
            raise ValueError(f"operator must be 'airflow_common_operators.JournalctlClean', got: {v}")
        return v


# Alias
JournalctlCleanOperator = JournalctlCleanTask
