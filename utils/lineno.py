
import inspect


def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno


__all__ = ['lineno']
