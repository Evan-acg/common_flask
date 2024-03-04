from typing import Any, Callable, Iterable, Iterator, List, Mapping, Sequence, Tuple
from wsgiref.headers import Headers
from wsgiref.types import StartResponse

from flask import Response

IHeaders = (
    Headers
    | Mapping[str, str | List[str] | Tuple[str, ...]]
    | Sequence[Tuple[str, str | List[str] | Tuple[str, ...]]]
)
IResponse = (
    Response
    | str
    | bytes
    | List[Any]
    | Mapping[str, Any]
    | Iterator[str]
    | Iterator[bytes]
)
IFlaskResponseRV = (
    Response
    | str
    | bytes
    | List[Any]
    | Mapping[str, Any]
    | Iterator[str]
    | Iterator[bytes]
    | Tuple[IResponse, IHeaders]
    | Tuple[IResponse, int]
    | Tuple[IResponse, int, IHeaders]
    | Callable[[dict[str, Any], StartResponse], Iterable[bytes]]
)
