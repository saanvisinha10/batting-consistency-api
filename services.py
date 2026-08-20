from schemas import ConsistencyRequest, ConsistencyResponse, DerivedVariables
from utils import calculate_stats

def compute_consistency_index(request: ConsistencyRequest) -> ConsistencyResponse:
    runs = [i.runs for i in request.innings]
    
    mean_runs, std_dev, cv, failures, failure_rate = calculate_stats(runs, request.failure_threshold)
    
    capped_cv = min(cv, 1.5) / 1.5
    penalty = (0.65 * capped_cv) + (0.35 * failure_rate)
    
    raw_score = max(0.0, (1.0 - penalty) * 100)
    consistency_index = round(raw_score, 2)
    
    if consistency_index >= 75:
        classification = "Highly Consistent"
        interpretation = f"{request.player_name} shows highly stable scoring patterns with low variance and minimal low-score failures."
    elif consistency_index >= 50:
        classification = "Moderately Stable"
        interpretation = f"{request.player_name} displays decent scoring regularity with occasional volatility across innings."
    elif consistency_index >= 30:
        classification = "Volatile"
        interpretation = f"{request.player_name} produces inconsistent outputs, alternating between big scores and frequent early dismissals."
    else:
        classification = "Highly Unstable"
        interpretation = f"{request.player_name} exhibits high scoring variance and high failure frequency under the current threshold."
        
    return ConsistencyResponse(
        player_id=request.player_id,
        player_name=request.player_name,
        innings_analyzed=len(runs),
        derived_variables=DerivedVariables(
            mean_runs=round(mean_runs, 2),
            std_dev=round(std_dev, 2),
            coefficient_of_variation=round(cv, 3),
            failure_count=failures,
            failure_rate=round(failure_rate, 3)
        ),
        consistency_index=consistency_index,
        classification=classification,
        interpretation=interpretation
    )
