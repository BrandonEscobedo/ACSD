from pydantic import BaseModel, Field


class MonitorConfigSchema(BaseModel):
    arrival_interval: float = Field(ge=1.0, le=60.0)
    buque_time: float = Field(ge=1.0, le=120.0)
    piso_time: float = Field(ge=1.0, le=120.0)
    max_containers: int = Field(ge=0, le=40)
    auto_advance: bool = True
