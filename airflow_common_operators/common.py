from shlex import quote as shell_quote

__all__ = ("in_bash", "in_conda", "in_virtualenv")


def in_bash(command: str, quote: str = "'", escape: bool = False, login: bool = True) -> str:
    """Run command inside bash.

    Args:
        command (str): string command to run
        quote (str, optional): Optional simple quoting, without escaping. May cause mismatched quote problems. Defaults to "'".
        escape (bool, optional): Full shell escaping. Defaults to False.
        login (bool, optional): Run in login shell (-l). Defaults to True.

    Returns:
        str: String command to run, starts with "bash"
    """
    if escape:
        command = shell_quote(command)
    if quote:
        command = f"{quote}{command}{quote}"
    if login:
        bash_flags = "-lc"
    else:
        bash_flags = "-c"
    return f"bash {bash_flags} {command}"


def in_conda(env: str, command: str, tool: str = "micromamba") -> str:
    return f"{tool} activate {env} && {command}"


def in_virtualenv(env: str, command: str) -> str:
    return f"source {env}/bin/activate && {command}"
