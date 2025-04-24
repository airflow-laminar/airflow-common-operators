from typing import Literal

from ccflow import BaseModel

Tool = Literal["pip", "uv"]


__all__ = ("BaseInstallable",)


class BaseInstallable(BaseModel):
    name: str
    install_deps: bool = False
    tool: Tool = "pip"
    virtualenv: str = ""
