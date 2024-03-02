# This module contains the `Entity` class, which is the base class for all mapper objects in the application.
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm

from ..utils.string_util import to_lower_camel_case


db: SQLAlchemy = SQLAlchemy()


class Entity(db.Model):
    __abstract__ = True
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createUserId = db.Column(
        db.Integer, nullable=False, name="create_user_id", default=-1
    )
    modifyUserId = db.Column(
        db.Integer, nullable=False, name="modify_user_id", default=-1
    )
    gmtCreate = db.Column(
        db.DateTime, nullable=False, name="gmt_create", default=db.func.now()
    )
    gmtModify = db.Column(
        db.DateTime,
        nullable=False,
        name="gmt_modify",
        default=db.func.now(),
        onupdate=db.func.now(),
    )
    status = db.Column(db.Integer, nullable=False, default=0)

    def __getitem__(self, item) -> any:
        """
        Retrieve the value of the specified attribute.

        Args:
            item (str): The name of the attribute to retrieve.

        Returns:
            any: The value of the specified attribute, or None if the attribute does not exist.
        """
        return getattr(self, item, None)

    def __str__(self) -> str:
        _items = [f"{k}={getattr(self, k)}" for k in self.keys()]
        return f"<{self.__class__.__name__}>({', '.join(_items)})"

    @orm.reconstructor
    def _init(self) -> None:
        """
        Initializes the Mapper object.

        Attributes:
        - use_low_camel_case (bool): Indicates whether to use low camel case for field names.
        - _extra_fields (List[str]): Extra fields for serialization.
        - _exclude_fields (List[str]): Fields to exclude from serialization.
        - _only_fields (List[str]): Fields to include for serialization.
        """
        self.use_low_camel_case: bool = True
        self._extra_fields: List[str] = []  # extra fields for serialization
        self._exclude_fields: List[str] = []  # exclude fields for serialization
        self._only_fields: List[str] = []  # only fields for serialization

    def keys(self):
        """
        Returns a list of keys representing the fields of the mapper object.

        If the `_only_fields` attribute is not empty, it returns the list of fields specified in `_only_fields`.
        Otherwise, it retrieves the keys from the `__table__.columns` attribute.
        If `use_low_camel_case` is True, the keys are converted to lower camel case using the `to_lower_camel_case` function.
        If `_exclude_fields` is a list and `_extra_fields` is not empty, the extra fields are added to the list of keys.
        Finally, it returns the list of keys excluding the fields specified in `_exclude_fields`.
        """
        if len(self._only_fields) > 0:
            return self._only_fields

        _items: List[str] = self.__table__.columns.keys()
        if self.use_low_camel_case:
            _items = [to_lower_camel_case(_) for _ in _items]

        if isinstance(self._exclude_fields, list) and len(self._extra_fields) > 0:
            _items.extend(self._extra_fields)

        return [item for item in _items if item not in self._exclude_fields]
