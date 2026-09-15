from fastapi import FastAPI

from backend.routes.scenario import router as scenario_router


app = FastAPI(
    title="UrbanTwin API",
    description="Backend API for the UrbanTwin urban digital twin prototype",
    version="1.0.0",
)


app.include_router(scenario_router)


@app.get("/")
def root():
    return {
        "message": "UrbanTwin API is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }