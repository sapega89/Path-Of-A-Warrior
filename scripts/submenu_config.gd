extends Node
## Конфіг для підменю: за menu_id викликає set_menu(title, links) на батьківському SubmenuShell.

@export var menu_id: int = 0

const CONFIGS: Array[Dictionary] = [
	{"title": "Mission", "links": []},
	{"title": "Blacksmith", "links": [{"label": "Buy Item", "action_id": 0}, {"label": "Sell Item", "action_id": 1}, {"label": "Cancel Sell", "action_id": 2}]},
	{"title": "Gamevil Live", "links": [{"label": "Coming Soon", "action_id": 0}]},
	{"title": "Visiting", "links": [{"label": "Select General", "action_id": 0}]},
	{"title": "Management", "links": [{"label": "Attributes", "action_id": 0}, {"label": "Skills", "action_id": 1}, {"label": "Gear", "action_id": 2}, {"label": "Inventory", "action_id": 3}]},
	{"title": "ETC", "links": [{"label": "Save", "action_id": 0}, {"label": "Load", "action_id": 1}]},
	{"title": "DIFFICULTY", "links": [{"label": "Hard", "action_id": 0}, {"label": "Normal", "action_id": 1}]},
]

func _ready() -> void:
	var shell: Control = get_parent()
	if not shell.has_method("set_menu"):
		return
	var idx := clampi(menu_id, 0, CONFIGS.size() - 1)
	var cfg: Dictionary = CONFIGS[idx]
	shell.set_menu(cfg.get("title", ""), cfg.get("links", []))
