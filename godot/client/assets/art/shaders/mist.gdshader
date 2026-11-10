shader_type spatial;
// Low mist over a marsh: a thin sheet of soft cloud in slow wisps, the colour of the dusk air,
// none inside a ring round the middle (the camp) so the mist lies over the water and the reeds.
// Several sheets one over another make it thick near the ground. Colours are sRGB.
render_mode unshaded, blend_mix, depth_draw_never, cull_disabled, shadows_disabled;

uniform vec3 color = vec3(0.3, 0.31, 0.38);
uniform float density = 0.3;
uniform vec2 centre = vec2(0.0);
uniform float clear_radius = 11.0;
uniform float seed = 0.0;

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

float fbm(vec2 p) {
	return noise(p) * 0.55 + noise(p * 2.13 + 7.1) * 0.3 + noise(p * 4.7 + 3.3) * 0.15;
}

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
	vec2 p = world_pos.xz;
	float n = fbm(p * vec2(0.14, 0.24) + vec2(TIME * 0.025, TIME * 0.01) + seed);
	float wisps = smoothstep(0.38, 0.78, n);
	float outside = smoothstep(clear_radius, clear_radius + 4.0, length(p - centre));
	ALBEDO = OUTPUT_IS_SRGB ? color : pow(color, vec3(2.2));
	ALPHA = clamp(density * wisps * outside, 0.0, 1.0);
}
