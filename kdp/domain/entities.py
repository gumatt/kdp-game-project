from typing import Self
from msgspec import Struct

from kdp.domain.value_objects import (
    ColumnValue,
    MapDirection,
    MapDimensionsOrdinal,
    MapLocationOrdinal,
    Mappable,
    RowValue,
    ValidationError)



class MapOrdinal(Struct):
    dimensions: MapDimensionsOrdinal
    objects: list[Mappable]

    @classmethod
    def factory(cls, rows: RowValue, columns: ColumnValue, objects: list[Mappable]) -> Self:
        if rows <= 0 or columns <= 0:
            raise ValidationError("rows and columns must be greater than 0")
        return cls(dimensions=MapDimensionsOrdinal(rows, columns), objects=objects)

    def place(self, obj: Mappable, row: RowValue, col: ColumnValue) -> None:
        if not self.valid_location(row, col):
            raise ValidationError(f"cannot place {obj.name} at {row}, {col}, no such location")
        if not self.object_fits(obj, row, col):
            raise ValidationError(f"cannot place {obj.name} at {row}, {col}, object does not fit")
        obj.location.row = row
        obj.location.column = col
        if obj not in self.objects:
            self.objects.append(obj)

    def move(self, obj: Mappable, row: RowValue, col: ColumnValue) -> None:
        if obj not in self.objects:
            raise ValidationError(f"cannot move {obj.name} to {row}, {col}, object not on map")
        if not self.valid_location(row, col):
            raise ValidationError(f"cannot move {obj.name} to {row}, {col}, no such location")
        if not self.object_fits(obj, row, col):
            raise ValidationError(f"cannot move {obj.name} to {row}, {col}, object does not fit")
        obj.location.row = row
        obj.location.column = col

    def valid_location(self, row: RowValue, col: ColumnValue) -> bool:
        return (
            row >= 1
            and col >= 1
            and row <= self.dimensions.rows
            and col <= self.dimensions.columns
        )

    def object_fits(self, obj: Mappable, row: RowValue, col: ColumnValue) -> bool:
        return (
            row + obj.size.rows <= self.dimensions.rows
            and col + obj.size.columns <= self.dimensions.columns
        )

class KDPMap(MapOrdinal):
    pass



class Villain(Struct):
    name: str
    map_info: Mappable

    @classmethod
    def factory(cls, name: str, row: RowValue, col: ColumnValue, direction: MapDirection, size: RowValue) -> Self:
        return cls(
            name=name,
            map_info=Mappable(
                location=MapLocationOrdinal(row, col),
                direction=direction,
                size=MapDimensionsOrdinal(size, size)
            )
        )

    @property
    def location(self) -> MapLocationOrdinal:
        return self.map_info.location

    @property
    def direction(self) -> MapDirection:
        return self.map_info.direction

    @property
    def size(self) -> MapDimensionsOrdinal:
        return self.map_info.size
