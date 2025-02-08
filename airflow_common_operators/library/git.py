from pydantic import BaseModel

from .common import Tool

__all__ = ("clone_repo", "GitRepo")


def clone_repo(name: str, repo: str, branch: str = "main", *, install: bool = True, install_deps: bool = False, tool: Tool = "pip"):
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
        tool = "uv pip" if tool == "uv" else "pip"
        install_deps_flag = "" if install_deps else "--no-deps "
        cmd = f"{tool} install {install_deps_flag}-e ."
        ret += f"\n{cmd}\n"
    return ret


class GitRepo(BaseModel):
    name: str
    repo: str
    branch: str = "main"

    install: bool = True
    install_deps: bool = False
    tool: Tool = "pip"

    def clone(self):
        return clone_repo(name=self.name, repo=self.repo, branch=self.branch, install=self.install, install_deps=self.install_deps, tool=self.tool)
