shader_type spatial;
// Worn painted figures: flat vertex colours from the palette, two-step light (a dull sun,
// deep cool shade, a thin rim of light on the edges turned from the camera), the grain and
// the worn patches of cloth and wood, and dust and mud rising from where a thing stands.

uniform vec3 shade_tint : source_color = vec3(0.56, 0.6, 0.78);
uniform float band_softness = 0.05;
uniform float shade_depth = 0.34;  // how much of the sun the shade keeps
uniform float grain = 0.1;
uniform float wear = 0.16;  // worn, darker patches
uniform float ground_shade = 0.12;
uniform vec3 dirt : source_color = vec3(0.4, 0.33, 0.25);  // dust and mud over the feet
uniform float dirt_height = 0.55;  // how high it rises (metres over the thing's origin); 0: none
uniform float rim = 0.18;
uniform vec3 tint : source_color = vec3(1.0);
uniform float flash = 0.0;
// the colour of a hit flash (white; the hero hit flashes red), in sRGB like the palette
uniform vec3 flash_color = vec3(1.0, 0.95, 0.85);
// 1 when the world is drawn as pixel art (Settings "pixel_art"): the light and the shadows in
// hard steps, a thin bright edge on the sun's side, and no grain finer than a pixel
global uniform float pixel_art;

varying vec3 world_pos;
varying float local_y;

float hash(vec3 p) {
	p = fract(p * 0.3183099 + 0.1);
	p *= 17.0;
	return fract(p.x * p.y * p.z * (p.x + p.y + p.z));
}

float noise(vec3 x) {
	vec3 i = floor(x);
	vec3 f = fract(x);
	f = f * f * (3.0 - 2.0 * f);
	return mix(mix(mix(hash(i), hash(i + vec3(1, 0, 0)), f.x), mix(hash(i + vec3(0, 1, 0)), hash(i + vec3(1, 1, 0)), f.x), f.y),
		mix(mix(hash(i + vec3(0, 0, 1)), hash(i + vec3(1, 0, 1)), f.x), mix(hash(i + vec3(0, 1, 1)), hash(i + vec3(1, 1, 1)), f.x), f.y), f.z);
}

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	local_y = world_pos.y - NODE_POSITION_WORLD.y;
}

vec3 to_srgb(vec3 c) {
	return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), c));
}

void fragment() {
	// vertex colours are linear (glTF); the Compatibility renderer takes ALBEDO in sRGB
	vec3 c = (OUTPUT_IS_SRGB ? to_srgb(COLOR.rgb) : COLOR.rgb) * tint;
	float coarse = noise(world_pos * vec3(9.0, 2.5, 9.0));
	float g = mix(coarse * 0.6 + noise(world_pos * 31.0) * 0.4, coarse * 0.8 + 0.1, pixel_art);
	c *= 1.0 - grain + grain * 2.0 * g;
	float w = smoothstep(0.35, 0.75, noise(world_pos * 3.1 + 7.0));
	c *= 1.0 - wear * w;
	c *= mix(1.0 - ground_shade, 1.0, smoothstep(0.0, 0.45, world_pos.y));
	vec3 mud = OUTPUT_IS_SRGB ? dirt : pow(dirt, vec3(2.2));
	float d = dirt_height > 0.0 ? 1.0 - smoothstep(0.0, dirt_height, local_y + (noise(world_pos * 6.0) - 0.5) * 0.18) : 0.0;
	c = mix(c, c * 0.45 + mud * 0.4, d * 0.75);
	vec3 fc = OUTPUT_IS_SRGB ? flash_color : pow(flash_color, vec3(2.2));
	ALBEDO = mix(c, fc, flash * 0.65);
	EMISSION = fc * flash * 0.45;
	ROUGHNESS = 1.0;
	SPECULAR = 0.0;
}

void light() {
	float ndl = dot(NORMAL, LIGHT);
	if (LIGHT_IS_DIRECTIONAL) {
		// the sun: two flat steps, and its cool tint in the shade
		float soft = max(band_softness * (1.0 - pixel_art), 0.001);
		float lit = smoothstep(0.0, soft, ndl) * 0.8 + smoothstep(0.45, 0.45 + soft, ndl) * 0.2;
		lit *= mix(smoothstep(0.2, 0.6, ATTENUATION), step(0.5, ATTENUATION), pixel_art);
		DIFFUSE_LIGHT += mix(shade_tint * shade_depth, vec3(1.0), lit) * LIGHT_COLOR / PI;
		// a thin rim where the surface turns away from the camera on the sun's side
		float edge = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 4.0);
		edge = mix(edge, step(0.3, edge) * 0.7, pixel_art);
		DIFFUSE_LIGHT += edge * rim * smoothstep(-0.2, 0.3, ndl) * LIGHT_COLOR;
	} else {
		// fires and lamps: plain light that fades with distance
		DIFFUSE_LIGHT += clamp(ndl, 0.0, 1.0) * ATTENUATION * LIGHT_COLOR / PI;
	}
}
