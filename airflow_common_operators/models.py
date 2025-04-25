from typing import List as PythonList

from pkn import Dict, List  # noqa: F401
from pydantic import BaseModel

from .common import in_bash

__all__ = (
    "List",
    "Dict",
    "BashCommands",
)


class BashCommands(BaseModel):
    commands: PythonList[str]

    def render(self, quote: str = "'", escape: bool = False, login: bool = True) -> str:
        return in_bash("\n".join(["set -ex"] + self.commands), quote=quote, escape=escape, login=login)
