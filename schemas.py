from pydantic import BaseModel, Field
from typing import List, Optional

class InningsInput(BaseModel):
    match_id: str
    runs: int = Field(..., ge=0, description="Runs scored in the innings")
    is_out: bool = Field(..., description="True if batter was dismissed")

class ConsistencyRequest(BaseModel):
    player_id: str
    player_name: str
    failure_threshold: Optional[int] = Field(default=10, ge=0, description="Runs threshold below which an innings is marked as a failure")
    innings: List[InningsInput] = Field(..., min_items=3, description="List of at least 3 recent innings")

class DerivedVariables(BaseModel):
    mean_runs: float
    std_dev: float
    coefficient_of_variation: float
    failure_count: int
    failure_rate: float

class ConsistencyResponse(BaseModel):
    player_id: str
    player_name: str
    innings_analyzed: int
    derived_variables: DerivedVariables
    consistency_index: float
    classification: str
    interpretation: str
