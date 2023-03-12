"""A tox plugin that allows backquote expansion in set_env section.
"""

from typing import Callable, Any

from tox.config.cli.parser import ToxParser
from tox.config.sets import EnvConfigSet
from tox.execute.api import Outcome, StdinSource
from tox.plugin import impl
from tox.session.state import State
from tox.tox_env.api import ToxEnv

EvalFunc = Callable[[ToxEnv, str], str]


SHELL = "bash"


def eval_cache_decorator(func: EvalFunc) -> EvalFunc:
    """A cache decorator for eval_backquote"""

    cache: dict[Any, str] = {}

    def _function(tox_env: ToxEnv, cmd: str) -> str:
        key = (tox_env, cmd)
        try:
            return cache[key]
        except KeyError:
            cache[key] = func(tox_env, cmd)
            return cache[key]

    return _function


def has_backticks(string: str) -> str | None:
    """If given parameter is a backquote string, then return the part inside
    the backquotes. Else return None, making the function result booleanish.
    """
    if len(string) > 2 and \
        string.startswith('`') and string.endswith('`'):
        return string[1:-1]
    return None


@eval_cache_decorator
def eval_backquote(tox_env: ToxEnv, cmd: str) -> str:
    """Evaluate a command inside a tox environment"""
    outcome = tox_env.execute([SHELL, "-c", cmd], StdinSource.OFF)
    return outcome.out.rstrip('\r\n')


# pylint: disable=protected-access

@impl
def tox_add_env_config(env_conf: EnvConfigSet, state: State) -> None:
    """Post process config after parsing."""
    for var, value in set_env._raw.items():
        if has_backticks(value):
            # Add bash in order to be able to evaluate backquotes.
            env_conf["allowlist_externals"].append(SHELL)
            return


@impl
def tox_before_run_commands(tox_env: ToxEnv) -> None:
    """Eval and replace backquotes expressions"""
    set_env = tox_env.conf["set_env"]
    for var, value in set_env._materialized.items():
        if cmd := has_backticks(value):
            set_env.update({var: eval_backquote(tox_env, cmd)})
