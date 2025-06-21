from datetime import datetime, timedelta
from typing import Optional, Type

from airflow.models import DagModel, DagRun
from airflow.operators.python import PythonOperator
from airflow.utils.session import provide_session
from airflow.utils.state import State
from airflow_pydantic import CallablePath, Task, TaskArgs
from pydantic import BaseModel, Field, field_validator
from pytz import UTC

__all__ = (
    "DagCleanupParams",
    "DagCleanupOperatorArgs",
    "DagCleanupTaskArgs",
    "DagCleanupOperator",
    "DagCleanupTask",
)


class DagCleanupParams(BaseModel):
    delete_successful: Optional[bool] = Field(default=True)
    delete_failed: Optional[bool] = Field(default=True)
    mark_failed_as_successful: Optional[bool] = Field(default=False)
    max_dagruns: Optional[int] = Field(default=10)
    days_to_keep: Optional[int] = Field(default=10)


class DagCleanupTaskArgs(DagCleanupParams, TaskArgs, extra="allow"): ...


# Alias
DagCleanupOperatorArgs = DagCleanupTaskArgs


def create_cleanup_dag_runs(**kwargs) -> PythonOperator:
    @provide_session
    def _cleanup_dag_runs(session=None, **context):
        params = context["params"]

        # Get the configurable parameters
        delete_successful = params.get("delete_successful", DagCleanupTaskArgs.model_fields["delete_successful"].default)
        delete_failed = params.get("delete_failed", DagCleanupTaskArgs.model_fields["delete_failed"].default)
        mark_failed_as_successful = params.get("mark_failed_as_successful", DagCleanupTaskArgs.model_fields["mark_failed_as_successful"].default)
        max_dagruns = params.get("max_dagruns", DagCleanupTaskArgs.model_fields["max_dagruns"].default)
        days_to_keep = params.get("days_to_keep", DagCleanupTaskArgs.model_fields["days_to_keep"].default)

        # Make cutoff_date timezone-aware (UTC)
        utc_now = datetime.utcnow().replace(tzinfo=UTC)
        cutoff_date = utc_now - timedelta(days=days_to_keep)

        # Fetch all DAGs from the DagBag
        dag_ids = [d.dag_id for d in session.query(DagModel.dag_id).distinct(DagModel.dag_id).all()]

        deleted = 0

        for dag_id in dag_ids:
            print(f"Cleaning up DAG: {dag_id}")

            # Query for DAG runs of each DAG
            query = session.query(DagRun).filter(DagRun.dag_id == dag_id)

            if delete_successful is False:
                query = query.filter(DagRun.state != State.SUCCESS)
            if delete_failed is False:
                query = query.filter(DagRun.state != State.FAILED)

            dagruns = query.order_by(DagRun.execution_date.asc()).all()
            total_runs = len(dagruns)

            for dr in dagruns:
                # Compare execution_date (offset-aware) with cutoff_date (now offset-aware)
                if dr.execution_date < cutoff_date or total_runs > max_dagruns:
                    session.delete(dr)
                    deleted += 1
                    total_runs -= 1  # Adjust count since we deleted one
                elif mark_failed_as_successful:
                    # Need to iterate through all remaining
                    if dr.state == State.FAILED:
                        # Mark failed runs as successful
                        dr.state = State.SUCCESS
                        session.merge(dr)
                elif not mark_failed_as_successful:
                    break  # Since they are ordered, no more to delete

        session.commit()
        print(f"Total DAG runs deleted: {deleted}")

    operator = PythonOperator(
        python_callable=_cleanup_dag_runs,
        **kwargs,
    )
    return operator


class DagCleanupTask(Task, DagCleanupTaskArgs):
    operator: CallablePath = Field(default="airflow_common_operators.tasks.dag_clean.create_cleanup_dag_runs", validate_default=True)

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, v: Type) -> Type:
        if v.__qualname__ != create_cleanup_dag_runs.__qualname__:
            raise ValueError(f"operator must be 'airflow_common_operators.tasks.dag_clean.create_cleanup_dag_runs', got: {v}")
        return v


# Alias
DagCleanupOperator = DagCleanupTask
