extends BaseScreen
## Blacksmith: Buy, Sell, Enchant and Combine, each a page of things (the shop screen).
## Combine with fewer than 3 things in the Inventory only says so. Enchant and Combine are only
## in the start camp (HeroRun.at_start); in the camps of a run their buttons are hidden and the
## blacksmith has the shop alone.

## Things the Inventory needs for Combine to open.
const COMBINE_AT_LEAST := 3
## The pages only the start camp has.
const START_ONLY := ["enchant", "combine"]
@onready var buttons: Array[Button] = [
	%Column.get_node("Buy"),
	%Column.get_node("Sell"),
	%Column.get_node("Enchant"),
	%Column.get_node("Combine"),
]
@onready var notice: AcceptDialog = %Notice


func _ready() -> void:
	var here := HeroRun.at_start(Profile.load_or_new(profile_path()))
	buttons[2].visible = here
	buttons[3].visible = here
	buttons[0].grab_focus.call_deferred()


## The page of `mode`; Enchant and Combine only in the start camp, Combine only with 3 things
## or more in the Inventory. False when it does not open.
func open_page(mode: String) -> bool:
	if mode in START_ONLY and not HeroRun.at_start(Profile.load_or_new(profile_path())):
		return false
	if mode == "combine" and things() < COMBINE_AT_LEAST:
		notice.popup_centered()
		return false
	var p := Router.params.duplicate()
	p["mode"] = mode
	Router.push("shop", p)
	return true


## The things in the hero's Inventory.
func things() -> int:
	var profile := Profile.load_or_new(profile_path())
	return profile.backpack.filter(func(it): return int(it.get("id", 0)) > 0).size()
