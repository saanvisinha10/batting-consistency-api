from typing import List
import numpy as np

def calculate_stats(runs_list: List[int], failure_threshold: int):
    arr = np.array(runs_list, dtype=float)
    mean_runs = float(np.mean(arr))
    std_dev = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    
    cv = (std_dev / mean_runs) if mean_runs > 0 else 2.0
    
    failures = int(np.sum(arr < failure_threshold))
    failure_rate = failures / len(arr)
    
    return mean_runs, std_dev, cv, failures, failure_rate
