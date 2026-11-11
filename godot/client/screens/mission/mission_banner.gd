class_name MissionBanner
extends PanelContainer
## The banner over the map: "Stage N" and "Stage N Complete", a thing acquired, the mission
## failed (with the gear it took) or won, and after a won mission the pages Total Exp and
## Time Exp with the exp bar under the text (the level gone up on it).

const WIDTH := 520
const TOP := 0.3  # its top, in parts of the screen's height

@onready var label: Label = $Lines/BannerText
@onready var exp_bar: ExpBar = $Lines/ExpBar  # on the pages Total Exp and Time Exp


## The banner of the page sim is on, hidden when there is none. run_line: on a failed
## mission, what it cost the run (a flask, or the run; HeroRun), "" for nothing.
func show_page(
	sim: MapSim, lord_name: String, mission_name: String, lost_gear: Dictionary, run_line: String
) -> void:
	visible = sim.banner != 0
	exp_bar.visible = sim.banner == MapSim.BANNER_TOTAL_EXP or sim.banner == MapSim.BANNER_TIME_EXP
	exp_bar.queue_redraw()
	if not visible:
		return
	if sim.banner == MapSim.BANNER_ACQUIRED:
		label.text = "%s\n%s" % [Items.name_of(sim.acquired), tr("mission.acquired")]
	else:
		label.text = "%s\n%s\n%s" % [lord_name, mission_name, _stage(sim, lost_gear, run_line)]
	var view := get_viewport_rect().size
	size = Vector2(WIDTH, 0)
	reset_size()
	position = Vector2((view.x - size.x) / 2.0, view.y * TOP)


## The banner's last lines: the stage, or how the mission ended.
func _stage(sim: MapSim, lost_gear: Dictionary, run_line: String) -> String:
	var stage := tr("mission.stage") + " " + str(sim.rooms_visited)
	if sim.banner == MapSim.BANNER_STAGE_CLEAR:
		stage += " " + tr("mission.complete")
	elif sim.banner == MapSim.BANNER_FAILED:
		stage = tr("mission.failed")
		if not run_line.is_empty():
			stage += "\n" + run_line
		if not lost_gear.is_empty():
			stage += "\n%s\n%s" % [tr("mission.lost"), Items.name_of(int(lost_gear.id))]
	elif sim.banner == MapSim.BANNER_SUCCESS:
		stage = "%s\n%s\n%d" % [tr("mission.success"), tr("mission.gold"), sim.gold_reward()]
	elif sim.banner == MapSim.BANNER_TOTAL_EXP or sim.banner == MapSim.BANNER_TIME_EXP:
		if sim.banner == MapSim.BANNER_TOTAL_EXP:
			stage = "%s\n%d" % [tr("mission.total_exp"), sim.exp_reward()]
		else:
			stage = (
				"%s\n%s %s\n%s %s"
				% [
					tr("mission.time_exp"),
					tr("mission.time_limit"),
					clock(sim.time_limit),
					tr("mission.time_taken"),
					clock(sim.play_seconds())
				]
			)
		if sim.exp_bars.level_up_ticks > 0:
			stage += "\n" + tr("mission.level_up") % sim.exp_bars.level
	return stage


## mm:ss
static func clock(secs: int) -> String:
	return "%02d:%02d" % [secs / 60, secs % 60]
