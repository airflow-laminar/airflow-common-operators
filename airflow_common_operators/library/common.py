from typing import Literal

Tool = Literal["pip", "uv"]


def in_conda_env(env: str, command: str, tool: str = "micromamba") -> str:
    return f""" {tool} activate {env} && {command} """


def in_virtual_env(env: str, command: str) -> str:
    return f""" source {env}/bin/activate && {command} """
