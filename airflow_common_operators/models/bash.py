from typing import List

from pydantic import BaseModel, model_serializer

__all__ = ("BashCommands",)


class BashCommands(BaseModel):
    commands: List[str]
    quote: str = "'"
    escape: bool = False
    login: bool = True

    @model_serializer()
    def _serialize(self) -> str:
        from airflow_common_operators import in_bash

        return in_bash("\n".join(["set -ex"] + self.commands), quote=self.quote, escape=self.escape, login=self.login)
