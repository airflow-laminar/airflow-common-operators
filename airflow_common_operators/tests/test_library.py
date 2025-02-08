from airflow_common_operators import GitRepo, PipLibrary, clone_repo, in_bash, in_conda, in_virtualenv


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

    def test_in_bash(self):
        assert in_bash('a simple "test"', escape=False, quote="'", login=True) == "bash -lc 'a simple \"test\"'"
        assert in_bash("a simple 'test'", escape=True, quote=False, login=False) == "bash -c 'a simple '\"'\"'test'\"'\"''"

    def test_in_conda(self):
        assert in_conda("a", "b") == "micromamba activate a && b"

    def test_in_virtualenv(self):
        assert in_virtualenv("a", "b") == "source a/bin/activate && b"
