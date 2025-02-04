from typing import List

from pydantic import BaseModel, Field

from .common import Tool
from .git import GitRepo

__all__ = ("PipLibrary", "LibraryList")


class PipLibrary(BaseModel):
    name: str
    version_constraint: str = ""

    tool: Tool = "pip"

    def install(self):
        tool = "uv pip" if self.tool == "uv" else "pip"
        return f"{tool} install {self.name}{self.version_constraint}"


class LibraryList(BaseModel):
    pip: List[PipLibrary] = Field(default_factory=list)
    git: List[GitRepo] = Field(default_factory=list)

    # def install(self):
    #     return "pip install " + " ".join(lib.name for lib in self.libraries)
