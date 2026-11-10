shader_type spatial;
// Grass and wheat (grass.gd): clumps of thin blades that sway in the wind. Gusts roll over the
// land the way the wind blows, so neighbouring clumps bend together, and each blade flutters a
// little on its own. A clump takes the colour of the ground it grows from (its instance's custom
// data: the colour, and in alpha how much lighter or darker this one is) and is lit as the
// ground (its normal points up), so it grows out of the land instead of standing on it.
// The vertex colour tells the blade's parts: red how high up (0 at the root, 1 at the tip),
// alpha 1 on an ear of wheat.
render_mode cull_disabled, world_vertex_coords;

uniform vec3 shade_tint : source_color = vec3(0.56, 0.6, 0.78);
// how much of the sun the shade keeps
uniform float shade_depth = 0.6;
// the way the wind blows over the land (x, z); its length is how hard
uniform vec2 wind = vec2(0.85, 0.5);
// how fast the gusts roll over the land, and how far apart they are (metres)
uniform float wind_speed = 0.35;
uniform float gust_size = 6.0;
// how far a tip bends in a full gust, for each metre of the blade's height
uniform float sway = 0.45;
// how much lighter a tip is than its root
uniform float tip_light = 0.55;
// the colour of the ears of wheat (sRGB)
uniform vec3 ear_colour : source_color = vec3(0.85, 0.7, 0.4);
// 1 when the world is drawn as pixel art (Settings "pixel_art"): the shadows' edges hard
global uniform float pixel_art;

varying float up;
varying float ear;
varying vec3 tint;

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
	vec3 root = MODEL_MATRIX[3].xyz;
	up = COLOR.r;
	ear = COLOR.a;
	float h = max(VERTEX.y - root.y, 0.0);
	float strength = length(wind);
	vec2 dir = strength > 0.0 ? wind / strength : vec2(1.0, 0.0);
	vec2 across = vec2(-dir.y, dir.x);
	// a gust: a band of wind rolling the way it blows, broken up along its front
	float front = dot(root.xz, dir) / gust_size - TIME * wind_speed;
	float gust = noise(vec2(front * 1.6, dot(root.xz, across) / (gust_size * 1.5)));
	gust = 0.2 + 0.8 * smoothstep(0.25, 0.85, gust);
	float flutter = sin(TIME * 2.7 + root.x * 4.1 + root.z * 3.3 + up * 1.7) * 0.12;
	float bend = (gust + flutter) * sway * strength * h * up;
	VERTEX.xz += dir * bend;
	VERTEX.y -= 0.5 * bend * bend / max(h, 0.05);
	NORMAL = vec3(0.0, 1.0, 0.0);
	tint = INSTANCE_CUSTOM.rgb * (0.85 + 0.3 * INSTANCE_CUSTOM.a);
}

void fragment() {
	vec3 c = tint * (1.0 - tip_light * 0.6 + tip_light * up);
	c = mix(c, ear_colour * (0.8 + 0.4 * up), ear);
	ALBEDO = OUTPUT_IS_SRGB ? c : pow(c, vec3(2.2));
	ROUGHNESS = 1.0;
	SPECULAR = 0.0;
}

void light() {
	if (LIGHT_IS_DIRECTIONAL) {
		float shadow = mix(smoothstep(0.2, 0.6, ATTENUATION), step(0.5, ATTENUATION), pixel_art);
		float lit = clamp(dot(NORMAL, LIGHT) * 2.0, 0.0, 1.0) * shadow;
		DIFFUSE_LIGHT += mix(shade_tint * shade_depth, vec3(1.0), lit) * LIGHT_COLOR / PI;
	} else {
		DIFFUSE_LIGHT += clamp(dot(NORMAL, LIGHT), 0.0, 1.0) * ATTENUATION * LIGHT_COLOR / PI;
	}
}
