import inspect
from typing import Callable


def get_function_module_path(func: Callable) -> str:
    """
    Utility function used to resolve a path argument to async_task/schedule function.

    It helps to avoid hard coding paths to functions, which might change in the future.

    Instead of:
        async_task('path.to.module.function', ...)

    Do this:
        from path.to.module import function

        async_task(get_function_module_path(function), ...)
    """

    return f"{inspect.getmodule(func).__name__}.{func.__name__}"
