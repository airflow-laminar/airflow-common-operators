from typing import Optional

from airflow_pydantic import CallablePath, ImportPath, PythonTask, PythonTaskArgs
from pydantic import Field

__all__ = (
    "SkipOperatorArgs",
    "SkipOperator",
    "FailOperatorArgs",
    "FailOperator",
    "PassOperatorArgs",
    "PassOperator",
)


class SkipTaskArgs(PythonTaskArgs):
    python_callable: Optional[CallablePath] = Field(default="airflow_common_operators.skip", description="python_callable")


# Alias
SkipOperatorArgs = SkipTaskArgs


class FailTaskArgs(PythonTaskArgs):
    python_callable: Optional[CallablePath] = Field(default="airflow_common_operators.fail", description="python_callable")


# Alias
FailOperatorArgs = FailTaskArgs


class PassTaskArgs(PythonTaskArgs):
    python_callable: Optional[CallablePath] = Field(default="airflow_common_operators.pass_", description="python_callable")


# Alias
PassOperatorArgs = PassTaskArgs


class SkipTask(PythonTask, SkipOperatorArgs):
    operator: ImportPath = Field(default="airflow_pydantic.airflow.PythonOperator", description="airflow operator path", validate_default=True)


# Alias
SkipOperator = SkipTask


class FailTask(PythonTask, FailOperatorArgs):
    operator: ImportPath = Field(default="airflow_pydantic.airflow.PythonOperator", description="airflow operator path", validate_default=True)


# Alias
FailOperator = FailTask


class PassTask(PythonTask, PassOperatorArgs):
    operator: ImportPath = Field(default="airflow_pydantic.airflow.PythonOperator", description="airflow operator path", validate_default=True)


# Alias
PassOperator = PassTask
