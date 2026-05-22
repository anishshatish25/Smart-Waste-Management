from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analytics import compute_command_center_metrics

app = FastAPI(
    title="Metropolitan AI Mesh Telemetry Node",
    description="Secure engine running optimized resource routing allocation.",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v3/urban/dispatch")
def get_optimized_metrics():
    return compute_command_center_metrics()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
