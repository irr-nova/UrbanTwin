import xml.etree.ElementTree as ET
import pandas as pd


def parse_edge_data(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    rows = []

    for interval in root.findall("interval"):
        interval_begin = interval.get("begin")
        interval_end = interval.get("end")

        for edge in interval.findall("edge"):
            row = {
                "edge_id": edge.get("id"),
                "interval_begin": interval_begin,
                "interval_end": interval_end,
                "sampled_seconds": edge.get("sampledSeconds"),
                "flow": edge.get("flow"),
                "speed": edge.get("speed"),
                "travel_time": edge.get("traveltime"),
                "waiting_time": edge.get("waitingTime"),
                "time_loss": edge.get("timeLoss"),
                "density": edge.get("density"),
                "occupancy": edge.get("occupancy"),
            }

            rows.append(row)

    df = pd.DataFrame(rows)

    numeric_columns = [
        "interval_begin",
        "interval_end",
        "sampled_seconds",
        "flow",
        "speed",
        "travel_time",
        "waiting_time",
        "time_loss",
        "density",
        "occupancy",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df[df["sampled_seconds"] > 0].copy()

    return df