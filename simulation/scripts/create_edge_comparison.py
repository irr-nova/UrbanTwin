import csv
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "simulation/scenarios/edgeData.xml"
SCENARIO = ROOT / "simulation/scenarios/edgeData.increased20.xml"
OUTPUT = ROOT / "simulation/outputs/edge_comparison.csv"

START, END = 0.0, 3600.0

# SUMO edgeData fields and their units.
METRICS = {
    "speed": ("m/s", True),
    "flow": ("vehicles/hour", True),
    "traveltime": ("seconds", True),
    "density": ("vehicles/km/lane", True),
    "timeLoss": ("seconds", True),
    "waitingTime": ("seconds", True),
    "occupancy": ("proportion", True),
    "sampledSeconds": ("seconds", False),
    "entered": ("vehicles", False),
    "left": ("vehicles", False),
    "departed": ("vehicles", False),
    "arrived": ("vehicles", False),
    "speedRelative": ("proportion", True),
    "laneDensity": ("vehicles/km/lane", True),
    "overlapDensity": ("vehicles/km/lane", True),
    "overlapTraveltime": ("seconds", True),
    "laneChangedFrom": ("vehicles", False),
    "laneChangedTo": ("vehicles", False),
}

def load_interval(path):
    root = ET.parse(path).getroot()
    matches = [
        interval for interval in root.findall("interval")
        if float(interval.get("begin", "-1")) == START
        and float(interval.get("end", "-1")) == END
    ]
    if len(matches) != 1:
        raise ValueError(
            f"{path.name}: expected exactly one interval "
            f"from {START} to {END}; found {len(matches)}"
        )

    edges = {}
    for edge in matches[0].findall("edge"):
        edge_id = edge.get("id")
        if not edge_id:
            continue
        if edge_id in edges:
            raise ValueError(f"Duplicate edge ID {edge_id} in {path.name}")
        edges[edge_id] = edge.attrib
    return edges

def number(record, field):
    raw = record.get(field)
    if raw is None or raw.strip() == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None

def fmt(value):
    if value is None:
        return ""
    return f"{value:.6f}".rstrip("0").rstrip(".")

def main():
    baseline = load_interval(BASELINE)
    scenario = load_interval(SCENARIO)
    ids = sorted(set(baseline) & set(scenario))

    columns = ["edge_id", "interval_begin_s", "interval_end_s"]
    for metric in METRICS:
        columns.extend([f"baseline_{metric}", f"scenario_{metric}"])
        if metric in {
            "speed", "flow", "traveltime", "density", "timeLoss"
        }:
            columns.extend([
                f"{metric}_abs_change",
                f"{metric}_change_pct",
            ])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for edge_id in ids:
            b, s = baseline[edge_id], scenario[edge_id]
            row = {
                "edge_id": edge_id,
                "interval_begin_s": fmt(START),
                "interval_end_s": fmt(END),
            }

            for metric in METRICS:
                bv, sv = number(b, metric), number(s, metric)
                row[f"baseline_{metric}"] = fmt(bv)
                row[f"scenario_{metric}"] = fmt(sv)

                if metric in {
                    "speed", "flow", "traveltime", "density", "timeLoss"
                }:
                    change = (
                        sv - bv if bv is not None and sv is not None
                        else None
                    )
                    pct = (
                        change / bv * 100
                        if change is not None and bv != 0
                        else None
                    )
                    row[f"{metric}_abs_change"] = fmt(change)
                    row[f"{metric}_change_pct"] = fmt(pct)

            writer.writerow(row)

    print(f"Baseline edge records: {len(baseline)}")
    print(f"Scenario edge records: {len(scenario)}")
    print(f"Matched edges exported: {len(ids)}")
    print(f"Interval: {START:.0f}-{END:.0f} seconds")
    print(f"CSV created: {OUTPUT}")

if __name__ == "__main__":
    main()
