class_name OnlineOptionsScreen
extends BaseScreen
## Multiplayer > Options: Invitation, Accept or Deny (pyport's Options > Invitation): whether
## another player's Challenge or Invite An Ally takes me into the battle. It is kept on the
## server.

var online: RefCounted
@onready var accept: Button = %Accept
@onready var deny: Button = %Deny
@onready var info: Label = %Info


func _ready() -> void:
	online = OnlineClient.of(Router.params)
	accept.grab_focus.call_deferred()
	if online == null:
		info.text = tr("live.failed")
		return
	info.text = tr("live.connecting")
	online.ask_options(OnlineClient.later(self, &"shown"))


func shown(err: String) -> void:
	if not err.is_empty():
		info.text = tr("live.failed")
		return
	info.text = tr("online.invitation_" + ("accept" if online.invitation == 1 else "deny"))
	accept.modulate = Color(1, 0.85, 0.4) if online.invitation == 1 else Color.WHITE
	deny.modulate = Color(1, 0.85, 0.4) if online.invitation == 0 else Color.WHITE


func choose(v: int) -> void:
	if online == null or online.busy:
		return
	info.text = tr("live.connecting")
	online.set_invitation(v, OnlineClient.later(self, &"shown"))
