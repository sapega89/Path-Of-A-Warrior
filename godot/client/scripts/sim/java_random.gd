extends RefCounted
## The game's random numbers: a 48-bit linear congruential generator (the same numbers as
## pyport/pow/midp/jrandom.py), so a fixed seed gives the same enemies and hits everywhere.

const MULT := 0x5DEECE66D
const MASK := (1 << 48) - 1

var seed := 0


func _init(s: int = -1) -> void:
	if s == -1:
		s = Time.get_ticks_usec() ^ int(Time.get_unix_time_from_system() * 1000.0)
	set_seed(s)


func set_seed(s: int) -> void:
	seed = (s ^ MULT) & MASK


## The next `bits` random bits as a signed 32-bit number.
func next_bits(bits: int) -> int:
	# seed * MULT mod 2^48, split so that no product leaves 64 bits
	var hi := seed >> 24
	var lo := seed & 0xFFFFFF
	seed = ((((hi * MULT) & 0xFFFFFF) << 24) + lo * MULT + 0xB) & MASK
	var v := (seed >> (48 - bits)) & 0xFFFFFFFF
	return v - 0x100000000 if v >= 0x80000000 else v


func next_int() -> int:
	return next_bits(32)


## A number in lo .. hi - 1 (as the game's rand_range).
func range_of(lo: int, hi: int) -> int:
	hi -= 1
	return lo + absi(next_int() % (absi(hi - lo) + 1))


## A number in 0 .. hi - 1.
func below(hi: int) -> int:
	return range_of(0, hi)
