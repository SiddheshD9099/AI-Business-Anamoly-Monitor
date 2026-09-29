METRIC_CONFIG = {

    "daily_transaction_volume": {
        "unit": "count",
        "direction": "neutral",
        "threshold": 20
    },

    "avg_transaction_value": {
        "unit": "currency",
        "direction": "neutral",
        "threshold": 20
    },

    "failed_transaction_rate": {
        "unit": "percentage",
        "direction": "lower_is_better",
        "threshold": 10
    },

    "chargeback_count": {
        "unit": "count",
        "direction": "lower_is_better",
        "threshold": 25
    },

    "loan_disbursal_amount": {
        "unit": "currency",
        "direction": "neutral",
        "threshold": 20
    },

    "npa_ratio": {
        "unit": "percentage",
        "direction": "lower_is_better",
        "threshold": 10
    }
}