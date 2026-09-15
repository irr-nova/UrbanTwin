from fastapi import APIRouter

from backend.schemas.scenario import ScenarioRequest
from backend.services.scenario_service import run_scenario


router = APIRouter(
    prefix="/scenario",
    tags=["Scenario"],
)


@router.post("/")
def create_scenario(request: ScenarioRequest):
    return run_scenario(
        approach=request.approach,
        traffic_change_percent=request.traffic_change_percent,
    )