shader_type canvas_item;
// The backdrop of a portrait: the colour of its side, light behind the head and darker to the
// corners, with soft strokes of paint and a fine grain.

uniform vec3 light_colour : source_color = vec3(0.85, 0.7, 0.42);
uniform vec3 dark_colour : source_color = vec3(0.43, 0.31, 0.16);

float hash(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 x) {
	vec2 i = floor(x);
	vec2 f = fract(x);
	f = f * f * (3.0 - 2.0 * f);
	return mix(mix(hash(i), hash(i + vec2(1, 0)), f.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), f.x), f.y);
}

void fragment() {
	vec2 uv = UV;
	float glow = 1.0 - smoothstep(0.05, 0.85, length((uv - vec2(0.5, 0.36)) * vec2(1.0, 1.15)));
	float strokes = noise(vec2(uv.x * 7.0 + uv.y * 3.0, uv.y * 16.0)) * 0.5 + noise(uv * 4.0) * 0.5;
	vec3 c = mix(dark_colour, light_colour, glow * (0.82 + 0.3 * strokes));
	c *= 0.96 + 0.08 * hash(floor(uv * 512.0));
	COLOR = vec4(c, 1.0);
}
