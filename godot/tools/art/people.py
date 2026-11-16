"""Which side each general of the campaign is on, for his model and his soldiers' on the map.

    python godot/tools/art/people.py     # writes godot/client/assets/art/people.json

The side follows the general's name: Crimean names (-bey, -murza, -aga, ...) are the horde,
Polish spelling is the Crown, the rest are Cossacks. OVERRIDES fixes the names the rule
gets wrong. Run it again when generals are added or renamed (data/campaign.json).
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAMPAIGN = os.path.join(ROOT, "client", "data", "campaign.json")
OUT = os.path.join(ROOT, "client", "assets", "art", "people.json")

HORDE = re.compile(r"-(bey|murza|aga|pasha|khan|sultan|mirza|efendi)\b|^kara-")
CROWN = re.compile(r"w|rz|sz|cz|^j|ski\b|cki\b|wicz")
OVERRIDES = {
    124: "crown",  # Roch Orlik
}


def side_of(name):
    n = name.lower()
    if HORDE.search(n):
        return "horde"
    if CROWN.search(n):
        return "crown"
    return "cossack"


def main():
    with open(CAMPAIGN, encoding="utf-8") as f:
        generals = json.load(f)["generals"]
    sides = {}
    for gid in sorted(generals, key=int):
        sides[gid] = OVERRIDES.get(int(gid), side_of(generals[gid]["name"]))
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"generals": sides}, f, indent=1, sort_keys=False)
        f.write("\n")
    counts = {s: list(sides.values()).count(s) for s in ("cossack", "crown", "horde")}
    print(f"{len(sides)} generals: {counts}")


if __name__ == "__main__":
    main()
