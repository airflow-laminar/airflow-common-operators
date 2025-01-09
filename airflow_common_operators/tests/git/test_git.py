from airflow_config import load_config


class TestConfig:
    def test_load_config_hydra(self):
        config = load_config(config_name="config")
        assert config
        assert "libraries" in config.extensions
        assert len(config.extensions["libraries"].pip) == 3
        assert len(config.extensions["libraries"].git) == 3
