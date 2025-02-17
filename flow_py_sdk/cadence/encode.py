import json
from typing import Any, Optional as Optional, Tuple, Callable, List

from flow_py_sdk.cadence.kind import Kind
from flow_py_sdk.cadence.types import Value


class CadenceJsonEncoder(json.JSONEncoder):
    def __init__(
        self,
        *,
        skipkeys: bool = ...,
        ensure_ascii: bool = ...,
        check_circular: bool = ...,
        allow_nan: bool = ...,
        sort_keys: bool = ...,
        indent: Optional[int] = ...,
        separators: Optional[Tuple[str, str]] = ...,
        default: Optional[Callable[..., Any]] = ...
    ) -> None:
        super().__init__(
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            default=default,
        )

    def default(self, o: Any) -> Any:
        if isinstance(o, Value):
            return o.encode()
        if isinstance(o, Kind):
            return o.encode()
        return super().default(o)


def encode_arguments(arguments: List[Value]) -> List[bytes]:
    if arguments is None:
        return []
    # the separators and the new line are there to get an identical json as the flow-go-sdk does (usually).
    # It doesn't need to be identical, but it is convenient for comparative testing with the go-sdk.
    return [
        (
            json.dumps(
                a, ensure_ascii=False, cls=CadenceJsonEncoder, separators=(",", ":")
            )
        ).encode("utf-8")
        for a in arguments
    ]
