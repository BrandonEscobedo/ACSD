from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.api.dependencies import get_monitor, get_ws_manager
from app.api.schemas.monitor import MonitorConfigSchema
from app.infrastructure.services.container_monitor import ContainerMonitor
from app.infrastructure.services.websocket_manager import WebSocketManager

router = APIRouter(tags=["monitor"])


# ── WebSocket ─────────────────────────────────────────────────────────────────

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    monitor: ContainerMonitor = Depends(get_monitor),
    ws_manager: WebSocketManager = Depends(get_ws_manager),
) -> None:
    await ws_manager.connect(websocket)
    try:
        await websocket.send_json(monitor.get_state())
        while True:
            await websocket.receive_text()  # keep-alive (client sends pings)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


# ── Control ───────────────────────────────────────────────────────────────────

@router.post("/api/monitor/start")
async def start_auto(monitor: ContainerMonitor = Depends(get_monitor)):
    await monitor.start_auto()
    return {"status": "started"}


@router.post("/api/monitor/stop")
async def stop_auto(monitor: ContainerMonitor = Depends(get_monitor)):
    await monitor.stop_auto()
    return {"status": "stopped"}


@router.put("/api/monitor/config")
async def update_config(
    cfg: MonitorConfigSchema,
    monitor: ContainerMonitor = Depends(get_monitor),
):
    monitor.config.arrival_interval = cfg.arrival_interval
    monitor.config.buque_time = cfg.buque_time
    monitor.config.piso_time = cfg.piso_time
    monitor.config.max_containers = cfg.max_containers
    monitor.config.auto_advance = cfg.auto_advance
    return {"status": "updated", "config": cfg.model_dump()}


@router.post("/api/monitor/add")
async def add_container(monitor: ContainerMonitor = Depends(get_monitor)):
    cont = await monitor.add_container()
    return {"status": "added", "id": cont.id}


@router.post("/api/monitor/advance/{container_id}")
async def advance_container(
    container_id: str,
    monitor: ContainerMonitor = Depends(get_monitor),
):
    ok = await monitor.advance_container(container_id)
    return {"status": "advanced" if ok else "not_found", "id": container_id}


@router.delete("/api/monitor/container/{container_id}")
async def remove_container(
    container_id: str,
    monitor: ContainerMonitor = Depends(get_monitor),
):
    ok = await monitor.remove_from_patio(container_id)
    return {"status": "removed" if ok else "failed", "id": container_id}


@router.post("/api/monitor/reset")
async def reset(monitor: ContainerMonitor = Depends(get_monitor)):
    await monitor.reset()
    return {"status": "reset"}


@router.get("/api/monitor/state")
async def get_state(monitor: ContainerMonitor = Depends(get_monitor)):
    return monitor.get_state()
