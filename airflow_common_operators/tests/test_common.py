from unittest.mock import patch

import pytest
from airflow.exceptions import AirflowFailException, AirflowSkipException

from airflow_common_operators import fail, pass_, ping, skip


class TestCommon:
    def test_pass(self):
        pass_()

    def test_skip(self):
        with pytest.raises(AirflowSkipException):
            skip()

    def test_fail(self):
        with pytest.raises(AirflowFailException):
            fail()

    def test_ping(self):
        assert ping("localhost")()
        with pytest.raises(AirflowSkipException):
            ping("nonexistent")()

    def test_ping_localappend(self):
        with patch("airflow_common_operators.common.call") as call:
            call.return_value = 0
            ping("blerg")()
            assert call.call_args[0][0] == ["ping", "-c", "1", "blerg.local"]