import xml.etree.ElementTree as ET
from pathlib import Path
import random

source = Path("simulation/routes/osm.passenger.trips.xml")
target = Path("simulation/routes/osm.passenger.trips.increased20.xml")

tree = ET.parse(source)
root = tree.getroot()

trips = root.findall("trip")
extra_count = round(len(trips) * 0.20)

random.seed(20)
selected = random.sample(trips, extra_count)

for index, original in enumerate(selected):
    extra = ET.Element("trip", original.attrib)
    extra.set("id", f"extra20_{index}")

    original_depart = float(original.get("depart", "0"))
    extra.set("depart", f"{original_depart + 1.0:.2f}")

    root.append(extra)

all_trips = root.findall("trip")
all_trips.sort(key=lambda trip: float(trip.get("depart", "0")))

for child in list(root):
    if child.tag == "trip":
        root.remove(child)

for trip in all_trips:
    root.append(trip)

tree.write(target, encoding="UTF-8", xml_declaration=True)

print(f"Original trips: {len(trips)}")
print(f"Additional trips: {extra_count}")
print(f"Total trips: {len(all_trips)}")
print("Trips sorted by departure time.")
print(f"Created: {target}")
