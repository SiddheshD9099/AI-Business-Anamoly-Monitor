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


def evaluate_failed_transactions_and_chargebacks(results):
    failed_rate = find_metric(
        results,
        "failed_transaction_rate"
    )
    chargebacks = find_metric(
        results,
        "chargeback_count"
    )

    if not failed_rate or not chargebacks:
        return None

    failed_rate_deviation = failed_rate.get(
        "baseline_deviation"
    )
    chargeback_deviation = chargebacks.get(
        "baseline_deviation"
    )

    if (
        failed_rate_deviation is not None
        and chargeback_deviation is not None
        and failed_rate_deviation >= 15
        and chargeback_deviation >= 15
    ):
        return {
            "type": "TRANSACTION_FAILURE_CHARGEBACK_SPIKE",
            "severity": "CRITICAL",
            "metrics": [
                "failed_transaction_rate",
                "chargeback_count"
            ],
            "observation": (
                "Failed transaction rate and chargeback count "
                "are both significantly above their recent baselines."
            ),
            "possible_implication": (
                "The joint increase may indicate a possible fraud "
                "pattern or a payment-processing issue requiring review."
            ),
            "recommended_checks": [
                "Review affected transactions for fraud indicators",
                "Compare chargebacks by payment channel and merchant",
                "Inspect issuer decline codes and payment gateway health",
                "Check authentication and dispute outcomes"
            ]
        }

    return None


def evaluate_disbursals_and_npa(results):
    disbursals = find_metric(
        results,
        "loan_disbursal_amount"
    )
    npa_ratio = find_metric(
        results,
        "npa_ratio"
    )

    if not disbursals or not npa_ratio:
        return None

    disbursal_deviation = disbursals.get(
        "baseline_deviation"
    )
    npa_deviation = npa_ratio.get(
        "baseline_deviation"
    )

    if (
        disbursal_deviation is not None
        and npa_deviation is not None
        and disbursal_deviation >= 15
        and npa_deviation >= 10
    ):
        return {
            "type": "DISBURSAL_NPA_RISK",
            "severity": "CRITICAL",
            "metrics": [
                "loan_disbursal_amount",
                "npa_ratio"
            ],
            "observation": (
                "Loan disbursal amount and NPA ratio are both "
                "above their recent baselines."
            ),
            "possible_implication": (
                "The concurrent increase may signal elevated "
                "underwriting or portfolio credit risk."
            ),
            "recommended_checks": [
                "Review recent underwriting policy and approval overrides",
                "Compare delinquency and NPA trends by origination cohort",
                "Check borrower, product, and geography concentrations",
                "Validate loan classification and provisioning data"
            ]
        }

    return None


def evaluate_transaction_concentration(results):
    average_value = find_metric(
        results,
        "avg_transaction_value"
    )
    transaction_volume = find_metric(
        results,
        "daily_transaction_volume"
    )

    if not average_value or not transaction_volume:
        return None

    average_value_deviation = average_value.get(
        "baseline_deviation"
    )
    volume_deviation = transaction_volume.get(
        "baseline_deviation"
    )

    if (
        average_value_deviation is not None
        and volume_deviation is not None
        and average_value_deviation >= 15
        and volume_deviation <= -10
    ):
        return {
            "type": "TRANSACTION_CONCENTRATION_RISK",
            "severity": "WARNING",
            "metrics": [
                "avg_transaction_value",
                "daily_transaction_volume"
            ],
            "observation": (
                "Average transaction value is above its recent baseline "
                "while daily transaction volume is below its baseline."
            ),
            "possible_implication": (
                "Activity may be concentrated in fewer or unusually "
                "large transactions, increasing exposure to individual "
                "counterparties or transactions."
            ),
            "recommended_checks": [
                "Review large-value transactions and counterparties",
                "Compare concentration by customer, channel, and geography",
                "Check for unusual account or transaction patterns",
                "Confirm monitoring limits and escalation controls"
            ]
        }

    return None


def evaluate_business_relationships(results):
    findings = []

    evaluators = [
        evaluate_failed_transactions_and_chargebacks,
        evaluate_disbursals_and_npa,
        evaluate_transaction_concentration
    ]

    for evaluator in evaluators:
        finding = evaluator(results)
        if finding:
            findings.append(finding)

    return findings
