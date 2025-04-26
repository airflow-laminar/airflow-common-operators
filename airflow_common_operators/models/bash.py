from typing import List

from pydantic import BaseModel

__all__ = ("BashCommands",)


class BashCommands(BaseModel):
    commands: List[str]

    def render(self, quote: str = "'", escape: bool = False, login: bool = True) -> str:
        from airflow_common_operators import in_bash

        return in_bash("\n".join(["set -ex"] + self.commands), quote=quote, escape=escape, login=login)
