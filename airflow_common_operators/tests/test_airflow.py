import pytest
from airflow.exceptions import AirflowFailException, AirflowSkipException

from airflow_common_operators import fail, pass_, skip


class TestCommon:
    def test_pass(self):
        pass_()

    def test_skip(self):
        with pytest.raises(AirflowSkipException):
            skip()

    def test_fail(self):
        with pytest.raises(AirflowFailException):
            fail()
