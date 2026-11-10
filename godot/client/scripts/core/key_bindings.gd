class_name KeyBindings
extends RefCounted
## The keys and pad buttons of the game actions, as the player has set them (Settings ->
## Controls, screens/controls/). Each action has its keys: the first one is the one the hints
## name and the player changes; the others (the arrows, the numeric keypad) work as well. An
## action that has a pad input has one: a button, or a trigger kept as TRIGGER + its axis.
##
## A key or a pad input does one thing. Given to another action, it is taken from the action
## that had it; when it was that action's first key or its pad input, that action gets the old
## one of the other in its place (the two swap), so nothing is left without a key. BACK and
## pause (Esc and Backspace; B and Start on a pad) are given to nothing, and pause itself does
## not change. On a pad SKIP is the AUTO button (the HUD's corner says which it is now), so it
## follows AUTO's.

const TRIGGER := 1000
const FIXED := ["pause"]
const BACK_KEYS := [KEY_ESCAPE, KEY_BACKSPACE]
const BACK_PAD := [JOY_BUTTON_B, JOY_BUTTON_START]
const TRIGGERS := [JOY_AXIS_TRIGGER_LEFT, JOY_AXIS_TRIGGER_RIGHT]
const PAD_FOLLOWS := {"skip": "auto"}

var keys := {}  # action -> Array of physical keycodes, the first one named by the hints
var pads := {}  # action -> its pad input (a JOY_BUTTON_*, or TRIGGER + a trigger's axis)
var _default_keys: Dictionary
var _default_pads: Dictionary


func _init(default_keys: Dictionary, default_pads: Dictionary) -> void:
	_default_keys = default_keys
	_default_pads = default_pads
	reset()


## The keys and buttons the game came with.
func reset() -> void:
	keys = {}
	for action in _default_keys:
		keys[action] = Array(_default_keys[action]).duplicate()
	pads = _default_pads.duplicate()


func can_change(action: String) -> bool:
	return keys.has(action) and not action in FIXED


## Whether the action has a pad input to change (the hero walks with the stick, fixed).
func can_change_pad(action: String) -> bool:
	return can_change(action) and pads.has(action) and not PAD_FOLLOWS.has(action)


## Makes `key` the action's first key. False (nothing changes) for BACK or for pause.
func bind_key(action: String, key: int) -> bool:
	if not can_change(action) or key == KEY_NONE or key in BACK_KEYS:
		return false
	var mine: Array = keys[action]
	var old: int = mine[0] if not mine.is_empty() else KEY_NONE
	if old == key:
		return true
	if mine.has(key):  # one of its other keys: now the one the hints name
		mine.erase(key)
		mine.push_front(key)
		return true
	for other in keys:
		var theirs: Array = keys[other]
		if other == action or not theirs.has(key):
			continue
		if theirs[0] == key and old != KEY_NONE:
			theirs.erase(old)
			theirs[0] = old
		else:
			theirs.erase(key)
	if mine.is_empty():
		mine.append(key)
	else:
		mine[0] = key
	return true


## Makes `pad` the action's pad input. False (nothing changes) for BACK, pause, or an action
## the pad does not change.
func bind_pad(action: String, pad: int) -> bool:
	if not can_change_pad(action) or pad in BACK_PAD:
		return false
	var old: int = pads[action]
	for other in pads:
		if pads[other] == pad:
			pads[other] = old
	pads[action] = pad
	_follow()
	return true


## What differs from the defaults, to keep in the settings: {"keys": {action: [keys]}, "pads":
## {action: pad}}; empty when nothing does.
func changes() -> Dictionary:
	var k := {}
	for action in keys:
		if keys[action] != Array(_default_keys[action]):
			k[action] = keys[action].duplicate()
	var p := {}
	for action in pads:
		if pads[action] != _default_pads[action]:
			p[action] = pads[action]
	if k.is_empty() and p.is_empty():
		return {}
	return {"keys": k, "pads": p}


## The defaults with the kept `changes()` on them; what is not a known action or a proper key
## or button is left out.
func take(kept: Variant) -> void:
	reset()
	if not kept is Dictionary:
		return
	var k: Variant = kept.get("keys", {})
	if k is Dictionary:
		for action in k:
			if can_change(str(action)) and _good_keys(k[action]):
				keys[str(action)] = Array(k[action]).map(func(c: Variant) -> int: return int(c))
	var p: Variant = kept.get("pads", {})
	if p is Dictionary:
		for action in p:
			if can_change_pad(str(action)) and typeof(p[action]) == TYPE_INT:
				if not int(p[action]) in BACK_PAD:
					pads[str(action)] = int(p[action])
	_follow()


func _follow() -> void:
	for action in PAD_FOLLOWS:
		if pads.has(action) and pads.has(PAD_FOLLOWS[action]):
			pads[action] = pads[PAD_FOLLOWS[action]]


static func _good_keys(list: Variant) -> bool:
	if not list is Array or list.is_empty():
		return false
	for c in list:
		if typeof(c) != TYPE_INT or c <= KEY_NONE or c in BACK_KEYS:
			return false
	return true


## The pad input of a trigger's axis.
static func trigger(axis: int) -> int:
	return TRIGGER + axis


## The InputEvent of a pad input, for every pad.
static func pad_event(pad: int) -> InputEvent:
	if pad >= TRIGGER:
		var m := InputEventJoypadMotion.new()
		m.axis = (pad - TRIGGER) as JoyAxis
		m.axis_value = 1.0
		return m
	var b := InputEventJoypadButton.new()
	b.button_index = pad as JoyButton
	return b
