import xml.etree.ElementTree as ET

import pandas as pd


COLUMNS = [
    "edge_id",
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

NUMERIC_COLUMNS = [
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


def parse_edge_data(xml_file):
    """Parse SUMO edgeData XML into a DataFrame of observed edges."""

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

    # Preserve a consistent set of columns even when no edges are present.
    df = pd.DataFrame(rows, columns=COLUMNS)

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Exclude edges with missing, invalid, or zero sampled duration.
    df = df[df["sampled_seconds"] > 0].copy()

    return df