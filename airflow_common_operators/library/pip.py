from typing import List, Optional

from pydantic import BaseModel, Field

from .common import Tool
from .git import GitRepo

__all__ = ("PipLibrary", "LibraryList")


class PipLibrary(BaseModel):
    name: str

    version_constraint: str = ""
    install_deps: bool = False
    tool: Tool = "pip"

    def install(self):
        tool = "uv pip" if self.tool == "uv" else "pip"
        install_deps_flag = "" if self.install_deps else "--no-deps "
        return f"{tool} install {install_deps_flag}{self.name}{self.version_constraint}"


class LibraryList(BaseModel):
    pip: List[PipLibrary] = Field(default_factory=list)
    git: List[GitRepo] = Field(default_factory=list)

    virtualenv: Optional[str] = ""

    # def install(self):
    #     return "pip install " + " ".join(lib.name for lib in self.libraries)
