from unittest.mock import MagicMock

from airflow_common_operators.models import BashCommands, DagCleanup


class TestModels:
    def test_bash(self):
        cmds = BashCommands(
            commands=[
                "echo 'hello world'",
                "echo 'goodbye world'",
            ]
        )
        assert cmds.render() == "bash -lc 'set -ex\necho 'hello world'\necho 'goodbye world''"

    def test_dag_cleanup(self):
        d = DagCleanup()
        d.cleanup_dag_runs(session=MagicMock(), params={})
