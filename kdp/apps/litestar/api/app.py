from typing import Any

from litestar import Controller, Litestar, get, post
from litestar.config.app import ExperimentalFeatures
from litestar.logging import StructLoggingConfig

from kdp.apps.litestar.api.models.definitions import KDPMapDTO
from kdp.domain.entities import KDPMap, Villain
from kdp.domain.value_objects import MapDirectionsOrdinal


class MapController(Controller):
    path = "/maps"

    @get("/{map_id:int}", return_dto=KDPMapDTO)
    async def get_map(self, map_id: int) -> KDPMap:
        try:
            villain = Villain.factory(
                name="Villiam",
                row=1,
                col=1,
                direction=MapDirectionsOrdinal.NORTH,
                size=1,
            )
        except Exception as e:
            print(f"Failed to create villain: {e}")
        return KDPMap.factory(rows=20, columns=35, objects=[villain])

    @post("/", return_dto=KDPMapDTO, body_dto=KDPMapDTO)
    async def create_map(self, data: KDPMap) -> KDPMap:
        try:
            my_data = data
            print(my_data)
            kdp_map = KDPMap.factory(
                rows=data.dimensions.rows,
                columns=data.dimensions.columns,
                objects=data.objects,
            )
        except Exception as e:
            print(f"Failed to create map: {e}")
        return kdp_map


@get("/")
async def index() -> dict[str, str]:
    return {"message": "Hello World!"}


app = Litestar(
    route_handlers=[index, MapController],
    experimental_features=[ExperimentalFeatures.DTO_CODEGEN],
)
