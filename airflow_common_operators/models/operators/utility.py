from typing import Optional

from airflow_pydantic import CallablePath, ImportPath, Task, TaskArgs
from pydantic import Field

__all__ = (
    "SkipOperatorArgs",
    "SkipOperator",
    "FailOperatorArgs",
    "FailOperator",
    "PassOperatorArgs",
    "PassOperator",
)


class SkipOperatorArgs(TaskArgs, extra="allow"):
    python_callable: Optional[CallablePath] = Field(default="airflow_common_operators.skip", description="python_callable")


class FailOperatorArgs(TaskArgs, extra="allow"):
    python_callable: Optional[CallablePath] = Field(default="airflow_common_operators.fail", description="python_callable")


class PassOperatorArgs(TaskArgs, extra="allow"):
    python_callable: Optional[CallablePath] = Field(default="airflow_common_operators.pass_", description="python_callable")


class SkipOperator(Task, SkipOperatorArgs):
    operator: ImportPath = Field(default="airflow.operators.python.PythonOperator", description="airflow operator path", validate_default=True)


class FailOperator(Task, FailOperatorArgs):
    operator: ImportPath = Field(default="airflow.operators.python.PythonOperator", description="airflow operator path", validate_default=True)


class PassOperator(Task, PassOperatorArgs):
    operator: ImportPath = Field(default="airflow.operators.python.PythonOperator", description="airflow operator path", validate_default=True)
