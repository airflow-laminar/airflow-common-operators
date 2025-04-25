from airflow_common_operators.models import BashCommands


class TestModels:
    def test_bash(self):
        cmds = BashCommands(
            commands=[
                "echo 'hello world'",
                "echo 'goodbye world'",
            ]
        )
        assert cmds.render() == "bash -lc 'set -ex\necho 'hello world'\necho 'goodbye world''"
