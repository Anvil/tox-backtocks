"""A tox plugin that allows backquote expansion in set_env section.
"""

from tox.config.cli.parser import ToxParser
from tox.config.sets import EnvConfigSet
from tox.execute.api import Outcome, StdinSource
from tox.plugin import impl
from tox.session.state import State
from tox.tox_env.api import ToxEnv


def has_backticks(string: str) -> str | None:
    """If given parameter is a backquote string, then return the part inside
    the backquotes. Else return None, making the function result booleanish.
    """
    if len(string) > 2 and \
        string.startswith('`') and string.endswith('`'):
        return string[1:-1]
    return None


# pylint: disable=protected-access


@impl
def tox_before_run_commands(tox_env: ToxEnv) -> None:
    """Eval and replace backquotes expressions"""
    set_env = tox_env.conf["set_env"]
    for var, value in set_env._materialized.items():
        if cmd := has_backticks(value):
            outcome = tox_env.execute(["bash", "-c", cmd], StdinSource.OFF)
            set_env.update({var: outcome.out.rstrip('\r\n')})
