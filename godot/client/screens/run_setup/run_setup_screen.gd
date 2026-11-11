class_name RunSetupScreen
extends BaseScreen
## Before the run, from the start camp's town hall: the starting skill, one of the first skills
## of the rows with its icon (two with the perk; HeroRun.choose_start_skill), and what fame buys
## there once and for good: the flasks of living water, a 4th gift card, a reroll of a gift each
## run and a second starting skill. Each with its price, or "bought". Every choice is saved at
## once.

## The buttons of the perks (HeroRun.PERK_PRICES) and the names they show.
const PERKS := {
	"card": ["Card", "run_setup.perk_card"],
	"reroll": ["Reroll", "run_setup.perk_reroll"],
	"second_skill": ["SecondSkill", "run_setup.perk_second_skill"],
}

var path: String = Profile.PATH
var profile: Profile
var skills := {}  # skill place -> its Button

@onready var fame: Label = %Fame
@onready var skills_title: Label = %SkillsTitle
@onready var flask: Button = %Flask
@onready var perk_list: VBoxContainer = %Perks


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
	for place: int in skills:
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


## Picks a starting skill and saves.
func choose(place: int) -> void:
	if profile.run.choose_start_skill(profile, place):
		profile.save(path)
	refresh()


func buy_flask() -> void:
	if profile.run.buy_flask(profile):
		profile.save(path)
	refresh()


func buy_perk(perk: String) -> void:
	if profile.run.buy_perk(profile, perk):
		profile.save(path)
	refresh()
