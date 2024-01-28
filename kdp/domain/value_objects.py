from typing import Annotated

from msgspec import Meta, Struct
from msgspec import ValidationError as VE  # noqa: N817

MapDirection = int
RowValue = int
ColumnValue = int
ValidationError = VE


class MapDirectionsOrdinal:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class MapLocationOrdinal(Struct):
    row: RowValue
    column: ColumnValue


class MapDimensionsOrdinal(Struct):
    rows: Annotated[RowValue, Meta(gt=0)]
    columns: Annotated[ColumnValue, Meta(gt=0)]


class Mappable(Struct):
    name: str
    location: MapLocationOrdinal
    direction: MapDirection
    size: MapDimensionsOrdinal
