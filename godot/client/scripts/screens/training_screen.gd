class_name TrainingScreen
extends "res://scripts/screens/mission_screen.gd"
## The training before the first mission (Andrey's choice: a training of its own, not hints in
## the mission): on the first mission's map a new hero walks, strikes, picks up loot, uses a
## skill, drinks a potion, turns on the auto-hunt, leaves a cleared room and pauses, one step at
## a time (scripts/ui/tutorial.gd). It is a mission screen with its own room: no time limit, no
## enemies but the ones a step sends, and nothing lost or kept (the hero is healed below a
## quarter of his HP; his exp, gold and loot stay here). After it, or Skip Training on the pause
## menu, the screen goes back and on to `then`: after New Game's opening story the game menu,
## from the Settings back to them.
## Params: {then (optional), then_params (optional, for `then`), profile_path (optional)}.

const LORD := 1
const SEED := 7  # the same soldiers every time

var tutorial: Tutorial
var then := ""
var then_params := {}


func mission_params() -> Dictionary:
	var p := {"lord": LORD, "mission": 0, "seed": SEED}
	if Router.params.has("profile_path"):
		p.profile_path = Router.params.profile_path
	return p


func _ready() -> void:
	then = str(Router.params.get("then", ""))
	then_params = Router.params.get("then_params", {})
	super._ready()
	sim.time_limit = 0
	sim.hold_room = true
	# the room as the training wants it: nobody in it (the mission's archers neither)
	sim.enemies.clear()
	sim.enemies_alive = 0
	for i in sim.waves.size():
		sim.waves[i] = 0
	_update_view(0.0)
	tutorial = Tutorial.new()
	tutorial.screen = self
	tutorial.finished.connect(leave)
	add_child(tutorial)


func _pause_menu_ready(menu: MissionPause) -> void:
	menu.leave = leave


## Back to where the training was opened from, and on to `then`.
func leave() -> void:
	set_process(false)
	if tutorial != null:
		tutorial.set_process(false)
	var next := then
	var next_params := then_params
	Router.back()
	if not next.is_empty():
		Router.push(next, next_params)
