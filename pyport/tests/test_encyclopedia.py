"""tools/gen_encyclopedia.py reads the game data the way the game does (tables of
docs/analysis/03 and 04) and the committed web/encyclopedia.html is up to date."""
import json
import pathlib
import re
import sys

import pytest

pytest.importorskip("PIL")
PY = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PY / "tools"))
import gen_encyclopedia as g  # noqa: E402


def test_tables():
    text = g.strings("text.scr")
    items = g.load_items()
    assert len(items) == 255 and items[101]["n"] == "Iron Blade" and items[518]["n"] == "Heaven's Belt"
    assert items[104]["lv"] == 45 and items[104]["s"] == {"ATK": "16–22"}
    gens = g.load_generals()
    assert len(gens) == 141 and sum(1 for x in gens.values() if x.get("visit")) == 44
    assert (gens[1]["n"], gens[1]["atk"], gens[1]["df"], gens[1]["hp"]) == ("Wallace", 4, 0, 20)
    scen, missions, rulers = g.load_missions(gens, text)
    assert len(scen) == 45 and len(missions) == 102 and len(rulers) == 22
    m = missions[12]                                    # Hellgate m4: Lord Wesley, ending E2
    assert (m["rn"], gens[m["boss"]]["n"], m["bl"], m["gold"], m["end"]) == \
        ("Lord Benjamin", "Lord Wesley", 7, 750, "Bloody Scarp")
    assert [s["rooms"] for s in scen[:4]] == [3, 3, 9, 12]
    assert len(g.load_recipes()) == 149


def test_page_is_current():
    page = (PY / "web" / "encyclopedia.html").read_text(encoding="utf-8")
    data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', page, re.DOTALL).group(1))
    assert len(data["items"]) == 255 and len(data["gens"]) == 141 and len(data["mis"]) == 102
