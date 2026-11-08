shader_type canvas_item;
// The backdrop of the menus in the grim look: soot-black, a little lighter in the middle and
// darker to the edges, mottled like old leather with a fine grain, and along the top and the
// bottom a strip of dark iron, brushed and rusted, with worn edges, a shadow under it and a
// rivet at every step. In pixels of the screen, so the strip keeps its size.

uniform vec3 middle : source_color = vec3(0.125, 0.118, 0.11);
uniform vec3 edge : source_color = vec3(0.035, 0.035, 0.04);
uniform vec3 iron : source_color = vec3(0.2, 0.192, 0.18);
uniform vec3 rivet : source_color = vec3(0.54, 0.52, 0.48);
uniform vec3 rust : source_color = vec3(0.3, 0.15, 0.08);
// how far the strip's middle is from the edge, its half height and the rivets' step (px)
uniform float band = 22.0;
uniform float half_height = 11.0;
uniform float step_px = 72.0;

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
	float glow = 1.0 - smoothstep(0.05, 0.9, length(centred * vec2(0.85, 1.2)));
	vec3 c = mix(edge, middle, glow);
	// old leather: soft blotches, small pebbles, a fine grain
	float blotch = noise(px / 160.0) * 0.6 + noise(px / 45.0) * 0.4;
	float pebble = noise(px / 5.0);
	c *= 0.78 + 0.34 * blotch - 0.08 * smoothstep(0.55, 0.9, pebble) + 0.05 * (hash(floor(px)) - 0.5);
	// the strip: d is the distance from its middle, toward the middle of the screen
	bool top = px.y < view.y * 0.5;
	float d = min(px.y, view.y - px.y) - band;
	float inside = 1.0 - smoothstep(half_height - 0.6, half_height + 0.6, abs(d));
	// its shadow on the leather
	float shade = smoothstep(half_height + 9.0, half_height, d) * step(half_height, d);
	c *= 1.0 - (top ? 0.55 : 0.3) * shade;
	// brushed along its length, spots of rust
	vec3 metal = iron * (0.8 + 0.35 * noise(px / vec2(55.0, 1.5)) + 0.08 * (hash(floor(px)) - 0.5));
	metal = mix(metal, rust, smoothstep(0.62, 0.85, noise(px / 18.0 + 7.0)) * 0.55);
	// the edge toward the light is worn bright, the other dark
	float up = top ? -d : d;
	float rim = smoothstep(half_height - 2.2, half_height - 0.6, abs(d));
	metal = mix(metal, up > 0.0 ? rivet * 0.7 : metal * 0.35, rim * 0.8);
	c = mix(c, metal, inside);
	// the rivets: a dark ring, a dome lit from the upper left
	float x = mod(px.x - view.x * 0.5, step_px) - step_px * 0.5;
	vec2 o = vec2(x, top ? d : -d);
	float r = length(o);
	float dome = 1.0 - smoothstep(4.6, 5.6, r);
	float lit = clamp(0.55 - dot(o, vec2(0.7, 0.7)) * 0.14, 0.12, 1.0);
	vec3 head = rivet * (0.35 + 0.75 * lit);
	head *= 1.0 - 0.5 * smoothstep(3.6, 5.0, r);
	c = mix(c, head, dome * inside);
	COLOR = vec4(c, 1.0);
}
