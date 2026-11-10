shader_type canvas_item;
// The smooth world (pixel_view.gd with pixel art off) at the brightness of the settings:
// world_gamma (1 as drawn, below 1 the shade lifted, over 1 deeper).

global uniform float world_gamma;

void fragment() {
	vec4 c = texture(TEXTURE, UV);
	COLOR = vec4(pow(c.rgb, vec3(world_gamma)), c.a);
}
