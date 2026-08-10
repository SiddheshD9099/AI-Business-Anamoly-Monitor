from src.anomaly_detector import detect_anomaly


result = detect_anomaly(
    current_value=150,
    baseline_value=100
)

print(result)