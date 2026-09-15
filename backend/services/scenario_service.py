def run_scenario(approach: str, traffic_change_percent: float):
    baseline = {
        "traffic_volume": 800,
        "average_speed": 31.2,
        "travel_time": 42.1,
        "fuel_consumption": 10.5,
        "co2_emissions": 25.4,
    }

    traffic_factor = 1 + (traffic_change_percent / 100)

    scenario = {
        "traffic_volume": round(
            baseline["traffic_volume"] * traffic_factor, 2
        ),
        "average_speed": round(
            baseline["average_speed"] * (1 - 0.003 * traffic_change_percent), 2
        ),
        "travel_time": round(
            baseline["travel_time"] * (1 + 0.005 * traffic_change_percent), 2
        ),
        "fuel_consumption": round(
            baseline["fuel_consumption"] * (1 + 0.004 * traffic_change_percent), 2
        ),
        "co2_emissions": round(
            baseline["co2_emissions"] * (1 + 0.004 * traffic_change_percent), 2
        ),
    }

    changes = {}

    for key in baseline:
        changes[key] = round(
            ((scenario[key] - baseline[key]) / baseline[key]) * 100,
            2,
        )

    return {
        "approach": approach,
        "traffic_change_percent": traffic_change_percent,
        "baseline": baseline,
        "scenario": scenario,
        "changes": changes,
        "ripple_chain": [
            "Traffic Volume",
            "Average Speed / Congestion",
            "Travel Time",
            "Fuel Consumption",
            "CO2 Emissions",
        ],
        "data_status": "mock_development_data",
    }