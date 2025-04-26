from unittest.mock import patch

import pytest
from airflow.exceptions import AirflowSkipException

from airflow_common_operators import ping


class TestCommon:
    def test_ping(self):
        assert ping("localhost")()
        with pytest.raises(AirflowSkipException):
            ping("nonexistent")()

    def test_ping_localappend(self):
        with patch("airflow_common_operators.utility.host.call") as call:
            call.return_value = 0
            ping("blerg")()
            assert call.call_args[0][0] == ["ping", "-c", "1", "blerg.local"]
