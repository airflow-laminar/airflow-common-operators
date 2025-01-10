from typing import List

from pydantic import BaseModel, Field

__all__ = ("clone_repo", "GitRepo", "PipLibrary", "LibraryList")


def clone_repo(name, repo, branch="main", install=True):
    ret = f"""
[[ -d {name} ]] || git clone {repo}
pushd {name}
git stash
git clean -fdx
git fetch --all --force
git checkout {branch}
git reset origin/{branch} --hard
"""
    if install:
        ret += """
pip install -e .
"""
    return ret


class GitRepo(BaseModel):
    name: str
    repo: str
    branch: str = "main"

    def clone(self, install: bool = True):
        return clone_repo(name=self.name, repo=self.repo, branch=self.branch, install=install)


class PipLibrary(BaseModel):
    name: str


class LibraryList(BaseModel):
    pip: List[PipLibrary] = Field(default_factory=list)
    git: List[GitRepo] = Field(default_factory=list)

    # def install(self):
    #     return "pip install " + " ".join(lib.name for lib in self.libraries)
