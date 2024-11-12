"""
by https://github.com/dmontagu
"""

from typing import TypeVar, Dict, Any, Generic, Type
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class DeferredModel(Generic[T]):
    def __init__(self, type_: Type[T], kwargs: Dict[str, Any]):
        self.type_ = type_
        self.kwargs = kwargs

    def validate(self) -> T:
        return self.type_(**self.kwargs)

    def __repr__(self):
        return (
            f"{type(self).__name__}(type_={self.type_.__name__}, kwargs={self.kwargs})"
        )


class DeferrableModel(BaseModel):
    @classmethod
    def defer(cls: Type[T], **kwargs: Any) -> DeferredModel[T]:
        return DeferredModel(cls, kwargs)
