"""Server managment endpoints."""
from aiolxd import LXD
from fastapi import APIRouter, Depends, Path, Query

from lxdapi.dependencies.lxd import get_lxd

router = APIRouter(tags=["server"], prefix="/server")


@router.get("/")
async def get_servers(
    *,
    lxd: LXD = Depends(get_lxd),
) -> list[str]:
    """Get servers."""
    servers = await lxd.instance.list(recursion=True)
    return [server.name for server in servers]


@router.post("/")
async def create_server(
    *,
    lxd: LXD = Depends(get_lxd),
    name: str = Query(..., min_length=1),
    source: str = Query(min_length=1, default="ubuntu/22.04"),
) -> str:
    """Create server."""
    creation_request = await lxd.instance.create(name=name, source=source, type_="virtual-machine")
    return creation_request.metadata["id"]


@router.delete("/{name}")
async def delete_server(
    *,
    lxd: LXD = Depends(get_lxd),
    name: str = Path(..., min_length=1),
) -> str:
    """Delete server."""
    deletion_request = await lxd.instance.delete(name=name)
    return deletion_request.metadata["id"]


@router.post("/{name}/start")
async def start_server(
    *,
    lxd: LXD = Depends(get_lxd),
    name: str = Path(..., min_length=1),
    force: bool = Query(False),
) -> str:
    """Start server."""
    start_request = await lxd.transport.instances.slash(name).state.put(data={"action": "start", "force": force})
    return start_request.metadata["id"]


@router.post("/{name}/stop")
async def stop_server(
    *,
    lxd: LXD = Depends(get_lxd),
    name: str = Path(..., min_length=1),
    force: bool = Query(False),
) -> str:
    """Stop server."""
    stop_request = await lxd.transport.instances.slash(name).state.put(data={"action": "stop", "force": force})
    return stop_request.metadata["id"]
