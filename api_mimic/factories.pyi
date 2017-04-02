from typing import Dict, Callable, Any


def mimic_factory(target: Dict[str, Callable[..., Any]]) -> type:
    ...


def init_func(self: Any, callback: Callable[[str, Dict[str, Any]], None]) -> None:
    ...
