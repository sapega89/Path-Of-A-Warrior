## Reads string resources from J2ME .scr binary files.
## Format: 2-byte LE count, then offset table (2 bytes LE per entry),
## then raw Modified-UTF-8 string data (same as UTF-8 for BMP chars).
class_name ScrReader

static func read_all(res_path: String) -> Array[String]:
	var file := FileAccess.open(res_path, FileAccess.READ)
	if file == null:
		push_warning("ScrReader: cannot open %s" % res_path)
		return []
	var data: PackedByteArray = file.get_buffer(file.get_length())
	file.close()
	if data.size() < 4:
		return []
	var count: int = data[0] | (data[1] << 8)
	var result: Array[String] = []
	for idx in range(count):
		var i: int = 2 + idx * 2
		if i + 4 > data.size():
			break
		var j: int = data[i] | (data[i + 1] << 8)
		var k: int = data[i + 2] | (data[i + 3] << 8)
		if j > data.size() or k > data.size() or k < j:
			result.append("")
			continue
		result.append(data.slice(j, k).get_string_from_utf8())
	return result
