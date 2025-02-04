from shlex import quote

__all__ = ("bash",)


def bash(command: str) -> str:
    return f"""bash -c "{quote(command)}" """
