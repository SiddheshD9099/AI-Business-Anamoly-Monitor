def detect_anomaly(
    current_value,
    baseline_value,
    warning_threshold=10,
    critical_threshold=20
):

    if baseline_value is None or baseline_value == 0:
        return {
            "status": "UNKNOWN",
            "change_percent": None
        }

    change_percent = (
        (current_value - baseline_value)
        / baseline_value
    ) * 100

    absolute_change = abs(change_percent)

    if absolute_change >= critical_threshold:

        status = "CRITICAL"

    elif absolute_change >= warning_threshold:

        status = "WARNING"

    else:

        status = "NORMAL"

    return {
        "status": status,
        "change_percent": change_percent
    }