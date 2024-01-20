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
    """Represents a map with ordinal dimensions and objects.

    Attributes:
        dimensions (MapDimensionsOrdinal): The dimensions of the map.
        objects (List[Mappable]): The list of objects placed on the map."""
    dimensions: MapDimensionsOrdinal
    objects: list[Mappable]

    @classmethod
    def factory(cls, rows: RowValue, columns: ColumnValue, objects: list[Mappable]) -> Self:
        if rows <= 0 or columns <= 0:
            raise ValidationError("rows and columns must be greater than 0")
        return cls(dimensions=MapDimensionsOrdinal(rows, columns), objects=objects)

    def move(self, obj: Mappable, row: RowValue, col: ColumnValue) -> None:
        """Moves an object on the map to the specified row and column.

        Args:
            obj (Mappable): The object to be moved on the map.
            row (RowValue): The row where the object should be moved.
            col (ColumnValue): The column where the object should be moved.

        Returns:
            None

        Raises:
            ValidationError: If the object is not on the map, the specified location is invalid, or the object does not fit."""
        if obj not in self.objects:
            raise ValidationError(f"cannot move {obj.name} to {row}, {col}, object not on map")
        if not self.valid_location(row, col):
            raise ValidationError(f"cannot move {obj.name} to {row}, {col}, no such location")
        if not self.object_fits(obj, row, col):
            raise ValidationError(f"cannot move {obj.name} to {row}, {col}, object does not fit")
        obj.location.row = row
        obj.location.column = col

    def place(self, obj: Mappable, row: RowValue, col: ColumnValue) -> None:
        """Places an object on the map at the specified row and column.

        Args:
            obj (Mappable): The object to be placed on the map.
            row (RowValue): The row where the object should be placed.
            col (ColumnValue): The column where the object should be placed.

        Returns:
            None

        Raises:
            ValidationError: If the specified location is invalid or the object does not fit."""
        if not self.valid_location(row, col):
            raise ValidationError(f"cannot place {obj.name} at {row}, {col}, no such location")
        if not self.object_fits(obj, row, col):
            raise ValidationError(f"cannot place {obj.name} at {row}, {col}, object does not fit")
        obj.location.row = row
        obj.location.column = col
        if obj not in self.objects:
            self.objects.append(obj)


    def valid_location(self, row: RowValue, col: ColumnValue) -> bool:
        """Checks if the specified row and column is a valid location on the map.

        Args:
            row (RowValue): The row to be checked.
            col (ColumnValue): The column to be checked.

        Returns:
            bool: True if the location is valid, False otherwise."""
        return (
            row >= 1
            and col >= 1
            and row <= self.dimensions.rows
            and col <= self.dimensions.columns
        )

    def object_fits(self, obj: Mappable, row: RowValue, col: ColumnValue) -> bool:
        """Checks if the specified object fits at the specified row and column on the map.

        Args:
            obj (Mappable): The object to be checked.
            row (RowValue): The row where the object should be placed or moved.
            col (ColumnValue): The column where the object should be placed or moved.

        Returns:
            bool: True if the object fits, False otherwise."""
        return (
            row + obj.size.rows <= self.dimensions.rows
            and col + obj.size.columns <= self.dimensions.columns
        )

class KDPMap(MapOrdinal):
    """
    Represents a KDP map, which is a specific type of MapOrdinal.
    """
    pass



class Villain(Mappable):
    """Represents a villain in the game.

    Attributes:
        name (str): The name of the villain.
        map_info (Mappable): The map information of the villain, including location, direction, and size.

    Methods:
        factory(cls, name: str, row: RowValue, col: ColumnValue, direction: MapDirection, size: RowValue) -> Self:
            Creates a new instance of Villain with the given name and map information."""
    name: str
    # map_info: Mappable

    @classmethod
    def factory(cls, name: str, row: RowValue, col: ColumnValue, direction: MapDirection, size: RowValue) -> Self:
        """"""
        return cls(
            name=name,
            location=MapLocationOrdinal(row, col),
            direction=direction,
            size=MapDimensionsOrdinal(size, size)
        )
