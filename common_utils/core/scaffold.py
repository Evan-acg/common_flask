import datetime
import decimal
import json
import logging
from math import ceil
from typing import Any

from flask import Flask as _Flask
from flask import Response, request
from flask.json.provider import DefaultJSONProvider

from common_utils.core.unify_exception import IException
from common_utils.core.unify_response import R, IResult
from common_utils.types.flask_type import IFlaskResponseRV


logger: logging.Logger = logging.getLogger("Flask")


class JSONProvider(DefaultJSONProvider):
    def dumps(self, o: Any, **kwargs: Any) -> str:
        print(o)
        if hasattr(o, "keys") and hasattr(o, "__getitem__"):
            o = dict(o)

        if isinstance(o, datetime.date):
            o = o.strftime("%Y-%m-%d")

        if isinstance(o, decimal.Decimal):
            o = float(o)

        if isinstance(o, bytes):
            o = o.decode("utf-8")

        return json.dumps(o, **kwargs)


class Flask(_Flask):
    json_provider_class = JSONProvider

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @self.errorhandler(404)
        def not_found(e):
            return R.fail(code=40400)

        @self.errorhandler(405)
        def not_allowed(e):
            return R.fail(code=40500)

        @self.errorhandler(500)
        def internal_server_error(e):
            return R.error()

        @self.errorhandler(Exception)
        def handle_exception(e):
            logger.exception(e)
            if isinstance(e, IException):
                return e.get_body()
            return R.error(message=str(e))

    def make_response(self, rv: IFlaskResponseRV) -> Response:
        if isinstance(rv, IResult):
            ret = rv
        else:
            ret = R.success()
            ret.data = rv

        ret.path = request.path
        ret.method = request.method
        _code: str = getattr(rv, "code", 20000)
        status: int = ceil(_code / 100)
        return super().make_response((dict(ret), status))
