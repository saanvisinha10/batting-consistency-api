from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ConsistencyRequest, ConsistencyResponse
from services import compute_consistency_index

app = FastAPI(
    title="Batting Consistency Index API",
    description="Calculates a batter's scoring stability using dispersion metrics and failure rates.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def root():
    return {"status": "live", "service": "Batting Consistency Index API"}

@app.post("/analytics/batting-consistency", response_model=ConsistencyResponse, tags=["Analytics"])
def get_batting_consistency(request: ConsistencyRequest):
    try:
        return compute_consistency_index(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
