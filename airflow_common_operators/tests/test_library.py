from airflow_common_operators import GitRepo, PipLibrary, clone_repo


class TestLibrary:
    def test_pip(self):
        p = PipLibrary(name="tmp", version_constraint="<5", install_deps=False, tool="uv")
        assert p.install() == "uv pip install --no-deps tmp<5"
        p = PipLibrary(name="tmp", version_constraint="", install_deps=True, tool="pip")
        assert p.install() == "pip install tmp"

    def test_git(self):
        g = GitRepo(name="tmp", repo="tmp", branch="main", install=True, install_deps=False, tool="uv")
        assert (
            g.clone()
            == "\n[[ -d tmp ]] || git clone tmp\npushd tmp\ngit stash\ngit clean -fdx\ngit fetch --all --force\ngit checkout main\ngit reset origin/main --hard\n\nuv pip install --no-deps -e .\n"
        )
        g = GitRepo(name="tmp", repo="tmp", branch="main", install=True, install_deps=True, tool="pip")
        assert (
            g.clone()
            == "\n[[ -d tmp ]] || git clone tmp\npushd tmp\ngit stash\ngit clean -fdx\ngit fetch --all --force\ngit checkout main\ngit reset origin/main --hard\n\npip install -e .\n"
        )
        assert (
            clone_repo(name="tmp", repo="tmp", branch="main", install=False, install_deps=True, tool="uv")
            == "\n[[ -d tmp ]] || git clone tmp\npushd tmp\ngit stash\ngit clean -fdx\ngit fetch --all --force\ngit checkout main\ngit reset origin/main --hard\n"
        )
