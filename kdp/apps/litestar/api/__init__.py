from litestar import Litestar, get



@get("/")
async def index() -> dict[str, str]:
    return {"message": "Hello World!"}


app = Litestar(route_handlers=[index])
