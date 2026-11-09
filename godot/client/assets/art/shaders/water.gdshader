shader_type spatial;
// Water of a map in the new art: the palette's blue, lighter bands of ripples drifting
// slowly and a few white glints. Colours are sRGB, like the palette.
render_mode unshaded, blend_mix, depth_draw_opaque, cull_disabled, shadows_disabled;

uniform vec3 deep = vec3(0.17, 0.29, 0.45);
uniform vec3 shallow = vec3(0.3, 0.46, 0.64);
uniform vec3 glint = vec3(0.86, 0.92, 0.96);

// The cells drawn (MapArt.show_only): a w x h mask over the map's rect (x, z, w, h); where it is
// 0 the place is darker, as the land around the map. No rect (w = 0): everything drawn.
uniform sampler2D view_mask : filter_linear, repeat_disable;
uniform vec4 view_rect = vec4(0.0);
uniform float hidden_shade = 0.5;

float shown_at(vec2 p) {
	if (view_rect.z <= 0.0) {
		return 1.0;
	}
	return texture(view_mask, (p - view_rect.xy) / view_rect.zw).r;
}

varying vec3 world_pos;

float hash(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 x) {
	vec2 i = floor(x);
	vec2 f = fract(x);
	f = f * f * (3.0 - 2.0 * f);
	return mix(mix(hash(i), hash(i + vec2(1, 0)), f.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), f.x), f.y);
}

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	vec2 p = world_pos.xz;
	float n = noise(p * 0.7 + vec2(TIME * 0.05, TIME * 0.03));
	float bands = smoothstep(0.55, 0.62, fract(p.y * 1.3 + n * 2.0 + TIME * 0.08)) * smoothstep(0.75, 0.62, fract(p.y * 1.3 + n * 2.0 + TIME * 0.08));
	float g = step(0.985, noise(p * 6.0 + vec2(TIME * 0.4, 0.0))) * noise(p * 1.3 - TIME * 0.2);
	vec3 c = mix(deep, shallow, n * 0.6 + bands * 0.5);
	c = mix(c, glint, clamp(g * 1.5, 0.0, 1.0));
	c *= mix(hidden_shade, 1.0, shown_at(world_pos.xz));
	ALBEDO = OUTPUT_IS_SRGB ? c : pow(c, vec3(2.2));
	ALPHA = 0.92;
}
