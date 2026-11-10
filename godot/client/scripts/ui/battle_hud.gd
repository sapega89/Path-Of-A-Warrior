class_name BattleHud
extends Control
## The HUD of the online battle (Hud of the battle screen): each fighter's plate at the top (my
## team at the left, the other at the right, one row under the other) with his portrait in an
## iron frame looking at the other side (Portrait0..3), his name, level on a cinnabar badge, HP
## and MP bars; the card of his action beside it; the changes of HP over the fighters; the
## quotes in parchment bubbles. The paint_* functions draw the HUD's pieces on any control.

const BOX_W := 360.0  # a fighter's plate at the top; the card of its action beside it
const BOX_H := 80.0
const FACE := 68.0  # the portrait on the plate
const CARD_W := 230.0
const PLATE := Color(0.07, 0.066, 0.062, 0.92)
const PAPER := Color("c9bb9b")  # old parchment
const HP_FILL := [Color("c23a2f"), Color("5e1510")]
const MP_FILL := [Color("5a83bd"), Color("1a2e55")]
const DAMAGE := Color("e8553f")
const HEAL := Color("8fc873")
## The change of HP rises from this many of the battle's pixels over the feet (and its own rise).
const DAMAGE_UP := 22.0
const QUOTE_UP := 66.0  # the quote's tail over the feet
## The icons of the battle's skills (3..13): their places on the sheet of the skills (the
## same skills of the map, 12..22).
const SKILL_ICONS := {3: 0, 4: 1, 5: 2, 6: 8, 7: 9, 8: 10, 9: 3, 10: 4, 11: 5, 12: 6, 13: 7}

var battle: RefCounted  # what is shown (scripts/net/online_battle.gd)
var camera: Camera3D  # the stage's: where the fighters are on screen
var portraits: Array[TextureRect] = []
var _icons := {}


func _ready() -> void:
	for i in 4:
		portraits.append(get_node("Portrait%d" % i) as TextureRect)


## An icon of the new art (assets/art/ui), drawn once at px.
func icon(icon_name: String, px := 64) -> Texture2D:
	var key := "%s %d" % [icon_name, px]
	if not _icons.has(key):
		_icons[key] = ArtHud.icon(icon_name, px)
	return _icons[key]


## Where fighter i's plate is: my team at the top left, the other at the top right, one row
## under the other.
func plate_rect(i: int, view: Vector2) -> Rect2:
	var f: RefCounted = battle.fighters[i]
	var x0 := view.x - 20.0 - BOX_W if f.mirrored() else 20.0
	return Rect2(x0, 14.0 + f.row() * (BOX_H + 12.0), BOX_W, BOX_H)


## The portraits on the plates, each looking towards the other side.
func show_portraits() -> void:
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		var face := portraits[i]
		face.visible = f.present
		if not f.present:
			continue
		var id := BattleMotion.portrait_of(f)
		face.texture = Pictures.portrait(id)
		# the hero's portraits look to the left, the others to the right
		var looks_left := id >= BattleMotion.HERO_PORTRAIT and id < BattleMotion.HERO_PORTRAIT + 4
		face.flip_h = looks_left != f.mirrored()
		var r := plate_rect(i, size)
		face.position = Vector2(
			r.end.x - 7.0 - FACE if f.mirrored() else r.position.x + 7.0, r.position.y + 6.0
		)
		face.modulate = Color(0.55, 0.55, 0.6) if f.hp <= 0 else Color.WHITE


## The fighters' plates, the cards of the actions beside them, the changes of HP over the
## fighters, the quotes.
func _draw() -> void:
	if battle == null:
		return
	for i in 4:
		var f: RefCounted = battle.fighters[i]
		if not f.present:
			continue
		var right: bool = f.mirrored()
		var r := plate_rect(i, size)
		var aimed: bool = battle.state == OnlineBattle.TARGET and i == battle.target_cursor
		paint_plaque(self, r, UiTheme.HIGHLIGHT if aimed else UiTheme.IRON, 3 if aimed else 2)
		var inner := Rect2(
			r.position + Vector2(0 if right else FACE + 16.0, 0),
			Vector2(r.size.x - FACE - 26.0, r.size.y)
		)
		var name: String = (
			f.name if f.alt_name.is_empty() or battle.round_no % 2 == 0 else f.alt_name
		)
		var badge := Vector2(
			inner.position.x + 22.0 if right else inner.end.x - 12.0, r.position.y + 22.0
		)
		var name_at := Vector2(inner.end.x if right else inner.position.x, r.position.y + 30.0)
		paint_text(
			self,
			name,
			name_at,
			22,
			UiTheme.HIGHLIGHT if aimed else UiTheme.TEXT,
			1 if right else -1
		)
		draw_circle(badge, 14.0, UiTheme.RED, true, -1.0, true)
		draw_arc(badge, 14.0, 0.0, TAU, 32, UiTheme.ACCENT, 2.0, true)
		paint_text(self, str(f.level), badge + Vector2(0, 6), 16, UiTheme.TEXT, 0)
		var bars := Rect2(inner.position.x + (10.0 if right else 0.0), 0, inner.size.x - 10.0, 0)
		paint_bar(
			self,
			Rect2(bars.position.x, r.position.y + 42, bars.size.x, 15),
			float(f.hp) / maxf(1.0, f.max_hp),
			HP_FILL,
			right
		)
		paint_bar(
			self,
			Rect2(bars.position.x, r.position.y + 62, bars.size.x, 9),
			float(f.mp) / 100.0,
			MP_FILL,
			right
		)
		var a: int = battle.card_action(i)
		if a >= 0:
			_card(
				f,
				a,
				Vector2(
					r.end.x + 10.0 if not right else r.position.x - 10.0 - CARD_W,
					r.position.y + 17.0
				)
			)
	for d in battle.damage_shown:
		var p := _screen_point(float(d[0]), float(d[1]), DAMAGE_UP + float(d[2]))
		var text := ("+%d" if int(d[3]) > 0 else "%d") % int(d[3])
		paint_text(self, text, p, 44, HEAL if int(d[3]) > 0 else DAMAGE, 0, 8)
	var side: int = battle.quote_side_shown()
	if side >= 0:
		for i in 4:
			if battle.says_quote(i, side):
				var f: RefCounted = battle.fighters[i]
				var q: String = f.quote_win if side == 2 else f.quote_start
				if not q.is_empty():
					var sx: float = (OnlineBattle.W - f.x) if f.mirrored() else f.x
					_quote(q, _screen_point(sx, f.y, QUOTE_UP))


func _screen_point(sx: float, y: float, up_px: float) -> Vector2:
	return camera.unproject_position(BattleStage.world_at(sx, y, up_px))


## A card of the action shown: a parchment plaque with the action's sign and its name; a
## target's card shows how the blow went.
func _card(f: RefCounted, a: int, at: Vector2) -> void:
	var r := Rect2(at, Vector2(CARD_W, 46))
	var sb := UiTheme.box(PAPER, UiTheme.INK, 2)
	sb.shadow_color = Color(0, 0, 0, 0.45)
	sb.shadow_size = 3
	draw_style_box(sb, r)
	var as_target: bool = (
		battle.state == OnlineBattle.TURN and battle.fighters.find(f) != battle.attacker
	)
	var sign := action_icon(a) if not (as_target and a == OnlineBattle.RES_HIT) else null
	if sign != null:
		draw_texture_rect(sign, Rect2(at + Vector2(8, 6), Vector2(34, 34)), false)
	elif as_target:
		paint_burst(self, at + Vector2(25, 23), 18.0, UiTheme.RED)  # the blow got through
	var text := action_name(a, as_target)
	draw_string(
		UiTheme.font("bold"),
		at + Vector2(52, 30),
		text,
		HORIZONTAL_ALIGNMENT_LEFT,
		CARD_W - 60,
		20,
		UiTheme.INK
	)


## The sign of an action: the sabre, the shield, the wind, a skill's medallion, the mace of
## auto-battle (a target's card: 2 evaded, the wind).
func action_icon(a: int) -> Texture2D:
	match a:
		0:
			return icon("sabre")
		1:
			return icon("shield")
		2:
			return icon("wind")
		OnlineBattle.AUTO:
			return icon("bulava")
	return ItemSlot.icon("skill", int(SKILL_ICONS[a])) if SKILL_ICONS.has(a) else null


func action_name(a: int, as_target: bool) -> String:
	if as_target:
		return tr("online.battle_hit") if a == OnlineBattle.RES_HIT else tr("online.battle_evaded")
	match a:
		0:
			return tr("online.battle_attack")
		1:
			return tr("online.battle_defend")
		2:
			return tr("online.battle_evade")
		OnlineBattle.AUTO:
			return tr("online.battle_auto")
	return OnlineClient.skill_name(a) if a >= 3 and a <= 13 else ""


## A quote in a parchment bubble over the speaker, its tail pointing down at him.
func _quote(q: String, tip: Vector2) -> void:
	var font := UiTheme.font("text")
	var sz := font.get_string_size(q, HORIZONTAL_ALIGNMENT_LEFT, -1, 24)
	var r := Rect2(tip.x - sz.x / 2.0 - 16.0, tip.y - 58.0, sz.x + 32.0, 44.0)
	r.position.x = clampf(r.position.x, 8.0, size.x - 8.0 - r.size.x)
	var tail := PackedVector2Array(
		[
			Vector2(tip.x - 10.0, r.end.y - 2.0),
			Vector2(tip.x + 10.0, r.end.y - 2.0),
			Vector2(tip.x, tip.y)
		]
	)
	var sb := UiTheme.box(PAPER, UiTheme.INK, 2)
	sb.set_corner_radius_all(4)
	sb.shadow_color = Color(0, 0, 0, 0.45)
	sb.shadow_size = 3
	draw_style_box(sb, r)
	draw_colored_polygon(tail, PAPER)
	draw_polyline(PackedVector2Array([tail[0], tail[2], tail[1]]), UiTheme.INK, 2.0, true)
	draw_string(
		font,
		Vector2(r.position.x + 16.0, r.position.y + 30.0),
		q,
		HORIZONTAL_ALIGNMENT_LEFT,
		-1,
		24,
		UiTheme.INK
	)


## A plaque: a dark plate with hard corners and a rim.
static func paint_plaque(layer: Control, r: Rect2, rim: Color, width: int) -> void:
	var sb := UiTheme.box(PLATE, rim, width)
	sb.shadow_color = Color(0, 0, 0, 0.5)
	sb.shadow_size = 5
	layer.draw_style_box(sb, r)


## A line of text in PT Sans Bold with a dark outline: align -1 from the point, 0 centred on
## it, 1 ending at it (the point is on the baseline).
static func paint_text(
	layer: Control,
	text: String,
	at: Vector2,
	px: int,
	color: Color,
	align: int,
	outline := 4,
	ink := UiTheme.INK
) -> void:
	var font := UiTheme.font("bold")
	var w := font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, px).x
	var p := at - Vector2(w * (align + 1) / 2.0, 0)
	if outline > 0:
		layer.draw_string_outline(font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, px, outline, ink)
	layer.draw_string(font, p, text, HORIZONTAL_ALIGNMENT_LEFT, -1, px, color)


## A bar in a dark hollow with an iron rim, filled from its outer end (a right plate's from the
## right), a light line along the top of the fill.
static func paint_bar(layer: Control, r: Rect2, part: float, fill: Array, right: bool) -> void:
	var back := UiTheme.box(UiTheme.SLOT, UiTheme.IRON, 1)
	layer.draw_style_box(back, r)
	part = clampf(part, 0.0, 1.0)
	if part <= 0.0:
		return
	var inner := r.grow(-2.0)
	var w := maxf(inner.size.y, inner.size.x * part)
	var at := Vector2(inner.end.x - w if right else inner.position.x, inner.position.y)
	var sb := UiTheme.box(fill[1])
	layer.draw_style_box(sb, Rect2(at, Vector2(w, inner.size.y)))
	var top := UiTheme.box(fill[0])
	layer.draw_style_box(top, Rect2(at, Vector2(w, inner.size.y * 0.62)))
	if w > inner.size.y:
		var shine := inner.size.y * 0.5
		layer.draw_line(
			at + Vector2(shine, 2.0), at + Vector2(w - shine, 2.0), Color(1, 1, 1, 0.35), 1.5, true
		)


## A star of light: eight rays.
static func paint_burst(layer: Control, c: Vector2, r: float, color: Color) -> void:
	var pts := PackedVector2Array()
	for k in 16:
		var a := k * TAU / 16.0 - PI / 2.0
		pts.append(c + Vector2(cos(a), sin(a)) * (r if k % 2 == 0 else r * 0.38))
	layer.draw_colored_polygon(pts, color)
	layer.draw_circle(c, r * 0.3, Color(1, 1, 1, 0.95), true, -1.0, true)
