extends "res://tests/test_case.gd"

const InputSetupScript := preload("res://scripts/core/input_setup.gd")


func test_actions_have_keys_and_pad() -> void:
	InputSetupScript.register()
	InputSetupScript.register()  # twice must not add duplicates
	for action in InputSetupScript.actions():
		check(InputMap.has_action(action), "%s missing" % action)
		var keys := 0
		var pad := 0
		for ev in InputMap.action_get_events(action):
			if ev is InputEventKey:
				keys += 1
			elif ev is InputEventJoypadButton or ev is InputEventJoypadMotion:
				pad += 1
		eq(keys, InputSetupScript.KEYS[action].size(), "%s keys" % action)
		check(pad >= 1, "%s has no gamepad binding" % action)
