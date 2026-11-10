class_name LiveSafeScreen
extends BaseScreen
## Game menu > Safe: gold between the hero (Local) and the Safe on the server. The arrow between
## the two (the menus' brass blade, assets/art/ui/safe_arrow.svg) says which way it goes, out of
## the Safe at first; it turns when pressed. The amount is typed in (no more than there is on
## that side) and OK moves it; the hero is saved then.

const ARROW := "safe_arrow"  # drawn pointing right, at the Safe
const ARROW_PX := 96

var live: RefCounted
var profile: RefCounted
var path: String = Profile.PATH
var to_safe := false  # the arrow points at the Safe (else at the hero)
var _arrows: Array[Texture2D] = [arrow_icon(false), arrow_icon(true)]
@onready var local: Label = %Local.get_node("Gold/Value")
@onready var server: Label = %Server.get_node("Gold/Value")
@onready var arrow: Button = %Arrow
@onready var amount: LineEdit = %Amount
@onready var ok: Button = %Ok
@onready var info: Label = %Info


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	live = LiveClient.of(Router.params)
	refresh()
	amount.grab_focus.call_deferred()
	if live == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	live.sync(profile, LiveClient.later(self, &"synced"))


func _on_amount_submitted(_t: String) -> void:
	submit()


func synced(err: String) -> void:
	refresh()
	info.text = "" if err.is_empty() else tr("live.failed")


## The gold on the side the arrow comes from.
func source() -> int:
	if to_safe:
		return int(profile.gold)
	return 0 if live == null else int(live.safe)


func turn() -> void:
	to_safe = not to_safe
	_typed(amount.text)
	refresh()


## Only digits, and no more than there is.
func _typed(t: String) -> void:
	var digits := ""
	for c in t:
		if c >= "0" and c <= "9":
			digits += c
	if not digits.is_empty():
		digits = str(mini(int(digits), source()))
	if digits != t:
		amount.text = digits
		amount.caret_column = digits.length()


## Moves the amount typed. Returns false when nothing was asked of the server.
func submit() -> bool:
	if live == null or live.busy or not live.synced:
		return false
	if source() == 0:
		info.text = tr("live.no_gold" if to_safe else "live.no_safe_gold")
		return false
	var n := int(amount.text)
	if n <= 0:
		return false
	live.move_gold(profile, to_safe, n, LiveClient.later(self, &"moved"))
	return true


func moved(err: String) -> void:
	if err.is_empty():
		profile.save(path)
		amount.text = ""
		info.text = ""
	else:
		info.text = tr("live.out_of_range" if err == "gold" else "live.failed")
	refresh()


func refresh() -> void:
	local.text = str(profile.gold)
	server.text = "-" if live == null or not live.synced else str(live.safe)
	arrow.icon = _arrows[1 if to_safe else 0]


## The arrow at the Safe (right) or at the hero (left).
static func arrow_icon(at_safe: bool) -> Texture2D:
	var tex := ArtHud.icon(ARROW, ARROW_PX)
	if at_safe:
		return tex
	var img := tex.get_image()
	img.flip_x()
	return ImageTexture.create_from_image(img)
