class_name RunEndScreen
extends BaseScreen
## The run is over (HeroRun): a mission lost with no flask left, or an ending that leads back to
## the start. What the hero keeps (his level, gold, fame and gear), what is gone (the skills of
## the run and the colonels' progress) and how many flasks are full again. The button, or back,
## goes on to the start camp.

@onready var kept: Label = %Kept
@onready var flasks: Label = %Flasks
@onready var go: Button = %Go


func _ready() -> void:
	var profile := Profile.load_or_new(profile_path()) as Profile
	kept.text = tr("run_end.kept") % [profile.level, profile.gold, profile.fame]
	flasks.text = tr("run_end.flasks") % profile.run.flasks_left
	go.grab_focus.call_deferred()
