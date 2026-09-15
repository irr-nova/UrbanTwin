from pydantic import BaseModel, Field


class ScenarioRequest(BaseModel):
    approach: str = Field(
        ...,
        description="Selected road approach"
    )

    traffic_change_percent: float = Field(
        ...,
        description="Change in traffic demand percentage"
    )