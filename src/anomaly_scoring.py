def calculate_anomaly_score(
    percentage_change,
    baseline_deviation,
    z_score
):
    """
    Calculate a simple anomaly score from
    multiple statistical signals.
    """

    score = 0

    # Signal 1: percentage change
    if percentage_change is not None:

        if abs(percentage_change) >= 20:
            score += 2

        elif abs(percentage_change) >= 10:
            score += 1

    # Signal 2: baseline deviation
    if baseline_deviation is not None:

        if abs(baseline_deviation) >= 20:
            score += 2

        elif abs(baseline_deviation) >= 10:
            score += 1

    # Signal 3: Z-score
    if z_score is not None:

        if abs(z_score) >= 3:
            score += 2

        elif abs(z_score) >= 2:
            score += 1

    return score

def determine_severity(score):

    if score >= 5:
        return "CRITICAL"

    elif score >= 3:
        return "WARNING"

    else:
        return "NORMAL"