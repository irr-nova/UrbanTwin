
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_SOURCE = ROOT / "simulation" / "routes" / "osm.passenger.trips.xml"
DEFAULT_OUTPUT_DIR = ROOT / "simulation" / "routes"


def main():
    parser = argparse.ArgumentParser(
        description="Generate a SUMO trip file with additional traffic."
    )
    parser.add_argument(
        "--percent",
        type=float,
        required=True,
        help="Percentage of additional trips, e.g. 10, 20, 30, or 90.",
    )
    parser.add_argument("--seed", type=int, default=20)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    if not 0 <= args.percent <= 1000:
        parser.error("Percent must be between 0 and 1000.")

    if not args.source.is_file():
        parser.error(f"Source trip file not found: {args.source}")

    tree = ET.parse(args.source)
    root = tree.getroot()

    original_trips = root.findall("trip")
    original_count = len(original_trips)

    if original_count == 0 and args.percent > 0:
        parser.error("No <trip> elements were found in the source file.")

    extra_count = round(original_count * args.percent / 100)
    rng = random.Random(args.seed)

    # Sample trips with replacement to create the requested number of extras.
    selected = rng.choices(original_trips, k=extra_count) if extra_count else []

    existing_ids = {
        trip.get("id")
        for trip in original_trips
        if trip.get("id") is not None
    }

    for index, original in enumerate(selected):
        extra = ET.Element("trip", original.attrib)

        # Ensure generated IDs do not collide with existing trip IDs.
        base_id = f"extra{args.percent:g}_{index}"
        new_id = base_id
        suffix = 1

        while new_id in existing_ids:
            new_id = f"{base_id}_{suffix}"
            suffix += 1

        extra.set("id", new_id)
        existing_ids.add(new_id)

        depart = float(original.get("depart", "0"))
        extra.set("depart", f"{depart + 1.0:.2f}")
        root.append(extra)

    # Collect and sort all trips by departure time.
    all_trips = root.findall("trip")
    all_trips.sort(key=lambda trip: float(trip.get("depart", "0")))

    # Record the first trip's position BEFORE removing any trips.
    children = list(root)
    first_trip_position = next(
        (i for i, child in enumerate(children) if child.tag == "trip"),
        len(children),
    )

    # Remove trips while preserving other XML elements, such as vType.
    for child in children:
        if child.tag == "trip":
            root.remove(child)

    # Reinsert the sorted trips at the original first-trip position.
    for offset, trip in enumerate(all_trips):
        root.insert(first_trip_position + offset, trip)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    percent_label = f"{args.percent:g}".replace(".", "p")
    target = (
        args.output_dir
        / f"osm.passenger.trips.increased{percent_label}.xml"
    )

    tree.write(target, encoding="UTF-8", xml_declaration=True)

    print(f"Original trips: {original_count}")
    print(f"Additional trips: {extra_count}")
    print(f"Total trips: {original_count + extra_count}")
    print(f"Traffic increase requested: {args.percent:g}%")
    print(f"Created: {target}")


if __name__ == "__main__":
    main()
