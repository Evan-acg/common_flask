from functools import wraps
from typing import List

from flask import request
from .mapper import User

from .unify_exception import Forbidden


def token_required(validator: callable = None):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if validator:
                if not validator(*args, **kwargs):
                    raise Forbidden()
                else:
                    return f(*args, **kwargs)
            else:
                token = request.headers.get("Authorization")
                if not token:
                    raise Forbidden()
                try:
                    User.parse_token(token)
                except Exception as e:
                    raise e
                return f(*args, **kwargs)

        return decorated

    return wrapper


def role_required(validation: callable):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not validation(*args, **kwargs):
                raise Forbidden()

            return f(*args, **kwargs)

        return decorated

    return wrapper
