__all__ = ("clone_repo",)


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
