class_name RunSetupScreen
extends BaseScreen
## Before the run, from the start camp's town hall: the starting skill, one of the first skills
## of the rows with its icon (two with the perk; HeroRun.choose_start_skill), only those the hero
## has learnt in a run (HeroRun.start_choices; the others are hidden), and what fame buys
## there once and for good: the flasks of living water, a 4th gift card, a reroll of a gift each
## run and a second starting skill. Each with its price, or "bought". Beside them, once an ending
## has led back to the start, the vows (Vows): the enemies' HP a step up per press, and three
## to take or give up, with what they add to the gold and fame. Every choice is saved at once.

## The buttons of the perks (HeroRun.PERK_PRICES) and the names they show.
const PERKS := {
	"card": ["Card", "run_setup.perk_card"],
	"reroll": ["Reroll", "run_setup.perk_reroll"],
	"second_skill": ["SecondSkill", "run_setup.perk_second_skill"],
}

## The buttons of the vows besides the enemies' HP (Vows.SWITCHES).
const VOW_BUTTONS := {
	"short_time": "ShortTime", "no_shop_potions": "NoShopPotions", "no_flasks": "NoFlasks"
}

var path: String = Profile.PATH
var profile: Profile
var skills := {}  # skill place -> its Button

@onready var fame: Label = %Fame
@onready var skills_title: Label = %SkillsTitle
@onready var flask: Button = %Flask
@onready var perk_list: VBoxContainer = %Perks
@onready var vow_list: VBoxContainer = %Vows
@onready var vows_title: Label = %VowsTitle


func _ready() -> void:
	path = profile_path()
	profile = Profile.load_or_new(path)
	for place: int in HeroRun.START_CHOICES:
		var b: Button = %Skills.get_node("Skill%d" % place)
		b.icon = ItemSlot.icon("skill", place)
		skills[place] = b
	refresh()
	skills[profile.run.start_skills[0]].grab_focus.call_deferred()


func refresh() -> void:
	var run: HeroRun = profile.run
	fame.text = tr("run_setup.fame") % profile.fame
	skills_title.text = tr(
		"run_setup.start_two" if run.has_perk("second_skill") else "run_setup.start_one"
	)
	var choices := run.start_choices(profile)
	for place: int in skills:
		skills[place].visible = place in choices
		skills[place].button_pressed = place in run.start_skills
	var price := run.flask_price()
	flask.text = (
		tr("run_setup.flask") % [run.flasks + 1, HeroRun.MAX_FLASKS, price]
		if price > 0
		else tr("run_setup.flasks_all")
	)
	flask.disabled = price == 0 or profile.fame < price
	for perk: String in PERKS:
		var b: Button = perk_list.get_node(PERKS[perk][0])
		var perk_name := tr(PERKS[perk][1])
		var cost := int(HeroRun.PERK_PRICES[perk])
		var bought := run.has_perk(perk)
		b.text = (
			tr("run_setup.bought") % perk_name
			if bought
			else tr("run_setup.price") % [perk_name, cost]
		)
		b.disabled = bought or profile.fame < cost
	_show_vows()


func _show_vows() -> void:
	var vows: Vows = profile.run.vows
	vow_list.visible = Vows.open(profile)
	vows_title.text = tr("run_setup.vows") % (vows.bonus_percent() - 100)
	vow_list.get_node("Hp").text = tr("vow.hp") % [vows.hp_steps, Vows.MAX_HP_STEPS]
	for vow: String in VOW_BUTTONS:
		var b: Button = vow_list.get_node(VOW_BUTTONS[vow])
		b.text = tr("vow.on") % tr("vow." + vow) if vows.has(vow) else tr("vow." + vow)


## Picks a starting skill and saves.
func choose(place: int) -> void:
	if profile.run.choose_start_skill(profile, place):
		profile.save(path)
	refresh()


func buy_flask() -> void:
	if profile.run.buy_flask(profile):
		profile.save(path)
	refresh()


func next_hp_step() -> void:
	profile.run.vows.next_hp_step()
	profile.save(path)
	refresh()


func switch_vow(vow: String) -> void:
	if profile.run.vows.switch(vow):
		profile.save(path)
	refresh()


func buy_perk(perk: String) -> void:
	if profile.run.buy_perk(profile, perk):
		profile.save(path)
	refresh()
