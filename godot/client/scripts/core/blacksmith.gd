class_name Blacksmith
extends RefCounted
## The Blacksmith of the camps: the shop (its potions and scrolls, and gear that changes after
## each mission won), selling, enchanting and combining. All of it is paid with the hero's gold
## and changes the hero (Profile).


## New things in the shop (after a mission won): its potions and scrolls, and 17 gears of the
## tiers the hero's level finds, the cheapest first.
static func fill_shop(hero: Profile, rng: RandomNumberGenerator = null) -> void:
	if rng == null:
		rng = RandomNumberGenerator.new()
	var ids: Array[int] = []
	for i in Items.SHOP_GEAR:
		ids.append(
			101 + 5 * rng.randi_range(0, 19) + Items.tier(hero.level, rng.randi_range(0, 99))
		)
	ids.sort()
	hero.shop = []
	for id in Items.SHOP_POTIONS:
		var it := Items.empty()
		it.id = id
		hero.shop.append(it)
	for id in ids:
		hero.shop.append(Items.make(id, rng))


## Buys thing i of the shop: a potion goes to its quick slot (5 at most), a gear to the
## backpack and out of the shop. Returns "bought", "no_gold", "no_more", "full" or "vow" (a
## potion under the vow of no shop potions, Vows).
static func buy(hero: Profile, i: int) -> String:
	if i < 0 or i >= hero.shop.size() or int(hero.shop[i].id) == 0:
		return ""
	var item: Dictionary = hero.shop[i]
	var cost := Items.price(item)
	var id := int(item.id)
	if id < 100 and hero.run.vows.has("no_shop_potions"):
		return "vow"
	if hero.gold < cost:
		return "no_gold"
	if id < 100:
		var slots := hero.quick_slots
		var at := -1
		for s in slots.size():
			if int(slots[s][0]) == id:
				at = s
				break
		if at >= 0:
			if int(slots[at][1]) >= 5:
				return "no_more"
			slots[at][1] = int(slots[at][1]) + 1
		else:
			for s in slots.size():
				if int(slots[s][0]) == 0:
					at = s
					break
			if at < 0:
				return "full"
			slots[at] = [id, 1]
	else:
		if not hero.add_item(item.duplicate()):
			return "full"
		hero.shop[i] = Items.empty()
	hero.gold -= cost
	return "bought"


## Sells a potion of quick slot i (where = "quick") or the thing in backpack place i, for
## half its price. False when there is nothing there.
static func sell(hero: Profile, where: String, i: int) -> bool:
	if where == "quick":
		var slots := hero.quick_slots
		if i < 0 or i >= slots.size() or int(slots[i][0]) == 0:
			return false
		hero.gold += Items.price({"id": int(slots[i][0])}) / 2
		if int(slots[i][1]) > 1:
			slots[i][1] = int(slots[i][1]) - 1
		else:
			slots[i] = [0, 0]
		return true
	if i < 0 or i >= hero.backpack.size() or int(hero.backpack[i].id) == 0:
		return false
	hero.gold += Items.price(hero.backpack[i]) / 2
	hero.backpack[i] = Items.empty()
	return true


## Whether a thing can be enchanted now: "ok", "not_possible" or "full" (enchanted as far
## as it goes).
static func can_enchant(item: Dictionary) -> String:
	var limit := Items.enchant_max(int(item.get("id", 0)))
	if limit <= 0:
		return "not_possible"
	if int(item.enchant) >= limit:
		return "full"
	return "ok"


## Enchants a thing of the backpack or the Gear page for its price: "success", "fail"
## (nothing happens), "lost" (the thing is gone) or "no_gold".
static func enchant(hero: Profile, item: Dictionary, rng: RandomNumberGenerator = null) -> String:
	if can_enchant(item) != "ok":
		return ""
	var cost := Items.enchant_price(item)
	if hero.gold < cost:
		return "no_gold"
	if rng == null:
		rng = RandomNumberGenerator.new()
	hero.gold -= cost
	var n := int(item.enchant)
	if rng.randi_range(1, 100) <= int(Items.ENCHANT_SUCCESS[n]):
		Items.enchant(item, rng)
		return "success"
	if rng.randi_range(0, 99) <= int(Items.ENCHANT_LOST[n]):
		var cleared := Items.empty()
		for k in cleared:
			item[k] = cleared[k]
		return "lost"
	return "fail"


## Combine: what three things of the backpack (places) would make, worked out when the third
## is chosen, as the Blacksmith tells it before asking: {} when they make nothing, else
## {"result": the new thing, "price": the fee, "success": whether it works (the new thing is
## then enchanted a third of their enchantings), "lost": the place lost when it fails, or -1}.
## A thing of a higher level is harder to make, and its failure loses more.
static func combine_plan(
	hero: Profile, places: Array, rng: RandomNumberGenerator = null
) -> Dictionary:
	if places.size() != 3:
		return {}
	if rng == null:
		rng = RandomNumberGenerator.new()
	var ids: Array = []
	var enchants := 0
	for p in places:
		var it: Dictionary = hero.backpack[int(p)]
		if int(it.id) <= 100:
			return {}
		ids.append(int(it.id))
		enchants += int(it.enchant)
	var results := Items.mixes(ids)
	if results.is_empty():
		return {}
	var id := int(results[rng.randi_range(0, results.size() - 1)])
	var result := Items.make(id, rng)
	var plan := {"result": result, "price": Items.price(result) / 4, "success": false, "lost": -1}
	var chance := (200 - Items.level_needed(id)) / 12
	if chance >= rng.randi_range(0, 100):
		plan.success = true
		for i in enchants / 3:
			Items.enchant(result, rng)
	else:
		var div := 15 if id < 500 else 12
		var lose := (100 - chance) * 10 / div
		if lose >= rng.randi_range(0, 100):
			plan.lost = int(places[rng.randi_range(0, 2)])
	return plan


## Pays for a planned Combine: the three things become the new one (in the third's place),
## or when it fails one of them may be lost. "success", "fail" or "no_gold".
static func combine(hero: Profile, places: Array, plan: Dictionary) -> String:
	if plan.is_empty():
		return ""
	if hero.gold < int(plan.price):
		return "no_gold"
	hero.gold -= int(plan.price)
	if plan.success:
		for p in places:
			hero.backpack[int(p)] = Items.empty()
		hero.backpack[int(places[2])] = (plan.result as Dictionary).duplicate()
		return "success"
	if int(plan.lost) >= 0:
		hero.backpack[int(plan.lost)] = Items.empty()
	return "fail"
