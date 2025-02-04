from pydantic import BaseModel

from .common import Tool

__all__ = ("clone_repo", "GitRepo")


def clone_repo(name, repo, branch="main", *, install=True, tool: Tool = "pip"):
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
        if tool == "uv":
            tool = "uv pip"
        ret += """
{tool} install -e .
"""
    return ret


class GitRepo(BaseModel):
    name: str
    repo: str
    branch: str = "main"

    def clone(self, install: bool = True, tool: Tool = "pip"):
        return clone_repo(name=self.name, repo=self.repo, branch=self.branch, install=install, tool=tool)
