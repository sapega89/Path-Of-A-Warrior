shader_type canvas_item;
// The round portrait of the art slice's HUD: the picture cut to a circle with a soft edge.

void fragment() {
	float d = distance(UV, vec2(0.5));
	COLOR = texture(TEXTURE, UV);
	COLOR.a *= 1.0 - smoothstep(0.47, 0.5, d);
}
