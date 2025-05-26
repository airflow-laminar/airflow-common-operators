from airflow.exceptions import AirflowFailException, AirflowSkipException

__all__ = (
    "skip",
    "fail",
    "pass_",
)


def skip():
    raise AirflowSkipException


def fail():
    raise AirflowFailException


def pass_():
    pass
