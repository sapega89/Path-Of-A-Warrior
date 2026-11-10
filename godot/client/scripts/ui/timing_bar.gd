class_name TimingBar
extends Control
## The timing bar of the online battle (Bar of the battle screen): the cursor runs to the gold
## mark; a click stops it, as the confirm key (stopped).

signal stopped

const BAR_SCALE := 4.0

var battle: RefCounted  # what is shown (scripts/net/online_battle.gd)


func _gui_input(e: InputEvent) -> void:
	if e is InputEventMouseButton and e.pressed:
		stopped.emit()


## The timing bar: a dark plate, the track from where the cursor starts past the gold mark,
## the run so far filling it from blue to gold, the cursor a bright blade. When it stopped:
## a gold burst on the mark for a perfect stop, Miss past it, else a flash where it stopped.
func _draw() -> void:
	if battle == null:
		return
	var s := BAR_SCALE
	BattleHud.paint_plaque(self, Rect2(Vector2.ZERO, size), UiTheme.IRON, 2)
	var left := 11.0 * s  # BAR_LEFT inside the plate (it is 110 px wide around CX)
	var mark := left + float(OnlineBattle.MARK - OnlineBattle.BAR_LEFT) * s
	var mid := size.y * 0.52
	var track := Rect2(left - 10.0, mid - 11.0, mark - left + 10.0 * s + 20.0, 22.0)
	var hollow := UiTheme.box(UiTheme.SLOT, UiTheme.IRON, 2)
	draw_style_box(hollow, track)
	var x := left + float(battle.bar_x - OnlineBattle.BAR_LEFT) * s
	var to := clampf(x, left, track.end.x - 4.0)
	if to > left:
		var k := clampf((to - left) / (mark - left), 0.0, 1.0)
		var tip := BattleHud.MP_FILL[0].lerp(UiTheme.ACCENT, k)
		draw_polygon(
			PackedVector2Array(
				[
					Vector2(left, mid - 6),
					Vector2(to, mid - 6),
					Vector2(to, mid + 6),
					Vector2(left, mid + 6)
				]
			),
			PackedColorArray(
				[BattleHud.MP_FILL[1], tip, tip.darkened(0.25), BattleHud.MP_FILL[1].darkened(0.3)]
			)
		)
	var to_item := get_canvas_item()
	var pulse := 1.15 if battle.state_ticks % 2 == 0 else 1.0
	UiTheme.rhombus(to_item, Vector2(mark, mid), 19.0 * pulse, UiTheme.INK)
	UiTheme.rhombus(to_item, Vector2(mark, mid), 16.0 * pulse, UiTheme.ACCENT)
	UiTheme.rhombus(to_item, Vector2(mark, mid), 7.0 * pulse, UiTheme.RED)
	var held: bool = battle.state == OnlineBattle.SENT and battle.bar_shown
	if held and battle.hit_score == 100:
		BattleHud.paint_burst(self, Vector2(mark, mid), 44.0, UiTheme.HIGHLIGHT)
		BattleHud.paint_text(
			self, tr("online.battle_perfect"), Vector2(size.x / 2.0, 30.0), 24, UiTheme.HIGHLIGHT, 0
		)
	elif held and battle.hit_score == 20:
		BattleHud.paint_text(
			self, tr("online.battle_miss"), Vector2(size.x / 2.0, 30.0), 24, BattleHud.DAMAGE, 0
		)
	elif held:
		BattleHud.paint_burst(self, Vector2(to, mid), 26.0, Color(1, 1, 1, 0.9))
	draw_line(Vector2(to, mid - 22.0), Vector2(to, mid + 22.0), UiTheme.INK, 7.0, true)
	draw_line(Vector2(to, mid - 20.0), Vector2(to, mid + 20.0), Color("efe4c8"), 3.0, true)
