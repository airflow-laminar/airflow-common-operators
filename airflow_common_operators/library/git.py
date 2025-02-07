from pydantic import BaseModel

from .common import Tool

__all__ = ("clone_repo", "GitRepo")


def clone_repo(name, repo, branch="main", *, install=True, tool: Tool = "pip", no_deps: bool = True):
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
        if no_deps:
            ret += f"""
{tool} install --no-deps -e .
"""
        else:
            ret += """
{tool} install -e .
"""
    return ret


class GitRepo(BaseModel):
    name: str
    repo: str
    branch: str = "main"

    install: bool = True
    tool: Tool = "pip"

    def clone(self):
        return clone_repo(name=self.name, repo=self.repo, branch=self.branch, install=self.install, tool=self.tool)
