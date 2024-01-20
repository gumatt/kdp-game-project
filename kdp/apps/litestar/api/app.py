from litestar import Controller, Litestar, get, post
from litestar.config.app import ExperimentalFeatures

from kdp.domain.entities import KDPMap



class MapController(Controller):
    path = "/maps"

    @get("/{map_id:str}")
    async def get_map(self, map_id: str) -> KDPMap:
        kdp_map = KDPMap.factory(rows=20, columns=35, objects=[25])
        return kdp_map

    @post("/")
    async def create_map(self, data: dict[str, int]) -> KDPMap:
        kdp_map = KDPMap.factory(rows=int(data['rows']), columns=int(data['cols']), objects=[])
        # kdp_map = KDPMap.factory(rows=20, columns=100, objects=[])
        return kdp_map



@get("/")
async def index() -> dict[str, str]:
    return {"message": "Hello World!"}


app = Litestar(
    route_handlers=[index, MapController],
    experimental_features=[ExperimentalFeatures.DTO_CODEGEN])
