shader_type canvas_item;
// The backdrop of the menus in the new art: dusk, lighter in the middle and darker to the
// edges, a grain like paper, and along the top and the bottom a band of folk rhombi (cinnabar
// in gold) between two thin gold lines. In pixels of the screen, so the band keeps its size.

uniform vec3 middle : source_color = vec3(0.157, 0.192, 0.271);
uniform vec3 edge : source_color = vec3(0.071, 0.086, 0.125);
uniform vec3 gold : source_color = vec3(0.831, 0.651, 0.271);
uniform vec3 cinnabar : source_color = vec3(0.659, 0.196, 0.176);
// how far the band's middle is from the edge, and its rhombi's step (px)
uniform float band = 26.0;
uniform float step_px = 34.0;

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
	vec2 view = 1.0 / SCREEN_PIXEL_SIZE;
	vec2 px = SCREEN_UV * view;
	vec2 centred = (SCREEN_UV - 0.5) * vec2(view.x / view.y, 1.0);
	float glow = 1.0 - smoothstep(0.1, 0.95, length(centred * vec2(0.9, 1.25)));
	vec3 c = mix(edge, middle, glow);
	// soft clouds of paint and a fine grain
	c *= 0.93 + 0.1 * noise(px / 140.0) + 0.04 * (hash(floor(px)) - 0.5);
	// the bands: the distance from the nearer edge, top or bottom
	float d = min(px.y, view.y - px.y) - band;
	float x = mod(px.x - view.x * 0.5, step_px) - step_px * 0.5;
	float diamond = abs(x) + abs(d) * 1.15;
	float inner = 1.0 - smoothstep(6.0, 7.2, diamond);
	float rim = (1.0 - smoothstep(9.0, 10.2, diamond)) * smoothstep(7.2, 8.4, diamond);
	float lines = 1.0 - smoothstep(0.4, 1.4, abs(abs(d) - 14.0));
	float dots = 1.0 - smoothstep(1.4, 2.6, length(vec2(abs(x) - step_px * 0.5, d)));
	c = mix(c, cinnabar, inner * 0.55);
	c = mix(c, gold, max(max(rim, dots) * 0.6, lines * 0.45));
	COLOR = vec4(c, 1.0);
}
