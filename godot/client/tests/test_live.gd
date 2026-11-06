extends "res://tests/test_case.gd"
## The game server parts. With POW_TEST_SERVER set (ws://..., CI starts godot/server) the
## client also logs in, saves and loads a hero there.

const NetClient := preload("res://scripts/core/net_client.gd")
const Profile := preload("res://scripts/core/profile.gd")
const ACCOUNT := "user://test_account.cfg"


func _client() -> Node:
	var n: Node = NetClient.new()
	n.account_path = ACCOUNT
	return n


func test_device_and_first_login() -> void:
	DirAccess.remove_absolute(ProjectSettings.globalize_path(ACCOUNT))
	var n := _client()
	var key: String = n.device_key()
	eq(key.length(), 32, "a random device key")
	eq(n.device_key(), key, "made once")
	eq(n.login_request(), ["guest_login", {"device": key}], "the first time as a guest")
	check(n.login_answered({"type": "guest_login_ok", "id": 1, "account": "gabc", "token": "t1"}), "logged in")
	eq(n.login_request(), ["login", {"account": "gabc", "token": "t1"}], "then with the token")
	check(not n.login_answered({"type": "error", "id": 2, "code": "login"}), "a refused login")
	n.free()


func test_no_server() -> void:
	var n := _client()
	n.open("ws://127.0.0.1:9")
	eq(str(n.ask_now("hello").get("code", "")), "offline", "no server there")
	n.free()


func test_hero_on_the_server() -> void:
	var url := OS.get_environment("POW_TEST_SERVER")
	if url.is_empty():
		return  # only where a server runs (CI)
	DirAccess.remove_absolute(ProjectSettings.globalize_path(ACCOUNT))
	var n := _client()
	check(n.open(url), "connecting")
	eq(str(n.ask_now("hello").type), "hello_ok", "the server answers")
	check(n.login_now(), "a guest login")
	var got: Dictionary = n.ask_now("hero_get")
	eq(got.hero, null, "a new account has no hero")
	var p := Profile.new()
	p.hero_name = "Cloud"
	p.gold = 777
	var put: Dictionary = n.ask_now("hero_put", {"hero": p.to_dict(), "rev": int(got.rev)})
	eq(str(put.type), "hero_put_ok", "saved")
	n.close()
	var m := _client()
	m.open(url)
	check(m.login_now(), "logged in again with the token")
	var back: Dictionary = m.ask_now("hero_get")
	var q := Profile.new()
	q.from_dict(back.hero)
	eq(q.hero_name, "Cloud", "the hero came back")
	eq(q.gold, 777, "with his gold")
	m.free()
	n.free()
