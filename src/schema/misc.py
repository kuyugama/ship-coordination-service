import typing
from .model import Schema, Field


__all__ = ["Paginated"]


class PaginationData(Schema):
    total: int = Field(ge=0, description="Total number of items")
    page: int = Field(ge=1, description="Number of page")
    pages: int = Field(ge=0, description="Total number of pages")


T_s = typing.TypeVar("T_s", bound=Schema)


class Paginated(Schema, typing.Generic[T_s]):
    __models__: dict[str, type[Schema]] = []

    pagination: PaginationData = Field(description="Information about the pagination")
    items: list[T_s] = Field(description="List of items")

    def __class_getitem__(cls, model: type[T_s]) -> type[Schema]:
        model_name = model.__qualname__ + "Pagination"

        if model_name in cls.__models__:
            return cls.__models__[model_name]

        fields = typing.cast(dict[str, typing.Any], Paginated.model_fields)

        model = typing.cast(
            type[Schema],
            type(
                model_name,
                (Schema,),
                dict(
                    __annotations__=dict(pagination=PaginationData, items=list[model]),
                    pagination=fields["pagination"],
                    items=fields["items"],
                ),
            ),
        )

        return model
