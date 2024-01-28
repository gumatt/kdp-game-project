from litestar.dto import DTOConfig
from litestar.dto.msgspec_dto import MsgspecDTO

from kdp.domain.entities import KDPMap, Villain
from kdp.domain.value_objects import Mappable


class KDPMapDTO(MsgspecDTO[KDPMap]):
    """
    Represents a KDP map, which is a specific type of MapOrdinal.
    """

    config = DTOConfig(
        rename_fields={"dimensions": "size"},
        max_nested_depth=2,
    )


class CreateKDPMapDTO(MsgspecDTO):
    """
    Represents a KDP map, which is a specific type of MapOrdinal.
    """

    rows: int
    cols: int
    objects: list[Mappable] = []


class VillainDTO(MsgspecDTO[Villain]):
    """Represents a Villain Data Transfer Object.

    This class is a subclass of MsgspecDTO and is used to represent a Villain in the application.
    It inherits all the attributes and methods from the parent class.
    """

    pass
