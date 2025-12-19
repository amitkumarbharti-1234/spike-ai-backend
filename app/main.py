from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.orchestrator.orchestrator import Orchestrator

app = FastAPI(
    title="Spike AI Backend",
    version="1.0.0"
)

# ----------------------
# Health Check
# ----------------------
@app.get("/")
def health():
    return {"status": "ok", "message": "Spike AI Backend is running"}

# ----------------------
# Request / Response Models
# ----------------------
class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query")
    propertyId: Optional[str] = Field(
        None, description="GA4 property ID (required for GA4 queries)"
    )

class QueryResponse(BaseModel):
    status: str
    data: dict

# ----------------------
# Main API Endpoint
# ----------------------
@app.post("/query", response_model=QueryResponse)
def query_handler(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    orchestrator = Orchestrator()
    result = orchestrator.route(
        query=request.query,
        property_id=request.propertyId
    )

    return QueryResponse(
        status="success",
        data=result
    )
