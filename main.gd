extends XROrigin3D

var midi_player : XRControllerMidiPlayer

func _ready():
	get_viewport().use_xr = true
	midi_player = $XRControllerMidiPlayer
	midi_player.xr_interfaces.append($XRController3D_r)
	midi_player.xr_interfaces.append($XRController3D_l)

func _on_xr_controller_3d_r_button_pressed(name):
	if (name == "trigger_click"):
		print("playing song...")
		midi_player.play()

func _on_xr_controller_3d_l_button_pressed(name):
	if (name == "trigger_click"):
		midi_player.stop()
