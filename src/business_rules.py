def find_metric(results, metric_name):

    for result in results:

        if result["metric"] == metric_name:
            return result

    return None

def get_change(result):
    return result.get("percentage_change")

def is_abnormal(result):
    return result["severity"] in [
        "WARNING",
        "CRITICAL"
    ]

def evaluate_business_relationships(results):

    findings = []

    traffic = find_metric(
        results,
        "Traffic"
    )

    conversion = find_metric(
        results,
        "Conversion_Rate"
    )

    orders = find_metric(
        results,
        "Orders"
    )

    revenue = find_metric(
        results,
        "Revenue"
    )

    cost = find_metric(
        results,
        "Cost"
    )

    refunds = find_metric(
        results,
        "Refunds"
    )

def evaluate_traffic_conversion(results):

    traffic = find_metric(
        results,
        "Traffic"
    )

    conversion = find_metric(
        results,
        "Conversion_Rate"
    )

    if not traffic or not conversion:
        return None

    traffic_baseline = (
        traffic["baseline_deviation"]
    )

    conversion_baseline = (
        conversion["baseline_deviation"]
    )

    if (
        traffic_baseline is not None
        and conversion_baseline is not None
        and traffic_baseline >= 15
        and conversion_baseline <= -10
    ):

        return {
            "type": "TRAFFIC_CONVERSION_MISMATCH",

            "severity": "CRITICAL",

            "metrics": [
                "Traffic",
                "Conversion_Rate"
            ],

            "observation": (
                "Traffic is significantly above its "
                "recent baseline while conversion rate "
                "is significantly below its baseline."
            ),

            "possible_implication": (
                "The additional traffic may be lower "
                "quality, or users may be encountering "
                "problems in the conversion funnel."
            ),

            "recommended_checks": [
                "Review traffic sources",
                "Check recent marketing campaigns",
                "Compare landing page conversion",
                "Check checkout and payment errors",
                "Review conversion by device"
            ]
        }

    return None

def evaluate_refunds(results):

    orders = find_metric(
        results,
        "Orders"
    )

    refunds = find_metric(
        results,
        "Refunds"
    )

    if not orders or not refunds:
        return None

    orders_change = orders[
        "percentage_change"
    ]

    refunds_change = refunds[
        "percentage_change"
    ]

    if (
        refunds_change is not None
        and orders_change is not None
        and refunds_change >= 30
        and refunds_change > orders_change
    ):

        return {
            "type": "REFUND_ACCELERATION",

            "severity": "CRITICAL",

            "metrics": [
                "Orders",
                "Refunds"
            ],

            "observation": (
                "Refunds are increasing substantially "
                "faster than orders."
            ),

            "possible_implication": (
                "This may indicate a deterioration in "
                "product quality, delivery performance, "
                "customer experience, or order accuracy."
            ),

            "recommended_checks": [
                "Review refund reasons",
                "Check product-level refund rates",
                "Review delivery failures",
                "Check customer complaints",
                "Compare refunds by product category"
            ]
        }

    return None

def evaluate_cost_revenue(results):

    revenue = find_metric(
        results,
        "Revenue"
    )

    cost = find_metric(
        results,
        "Cost"
    )

    if not revenue or not cost:
        return None

    revenue_change = revenue[
        "percentage_change"
    ]

    cost_change = cost[
        "percentage_change"
    ]

    if (
        revenue_change is not None
        and cost_change is not None
        and cost_change >= 20
        and cost_change > revenue_change
    ):

        return {
            "type": "COST_REVENUE_MISMATCH",

            "severity": "WARNING",

            "metrics": [
                "Revenue",
                "Cost"
            ],

            "observation": (
                "Costs are increasing faster than "
                "revenue."
            ),

            "possible_implication": (
                "Profitability may be deteriorating "
                "even if revenue is increasing."
            ),

            "recommended_checks": [
                "Review acquisition costs",
                "Check advertising spend",
                "Analyze cost by channel",
                "Calculate contribution margin"
            ]
        }

    return None

def evaluate_business_relationships(results):

    findings = []

    traffic_finding = (
        evaluate_traffic_conversion(results)
    )

    if traffic_finding:
        findings.append(traffic_finding)

    refund_finding = (
        evaluate_refunds(results)
    )

    if refund_finding:
        findings.append(refund_finding)

    cost_finding = (
        evaluate_cost_revenue(results)
    )

    if cost_finding:
        findings.append(cost_finding)

    return findings

