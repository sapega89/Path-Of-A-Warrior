shader_type spatial;
// Painted wood: flat vertex colours from the palette, two-step light (warm sun, cool
// shade), a faint brush grain and a darker foot where things touch the ground.

uniform vec3 shade_tint : source_color = vec3(0.56, 0.6, 0.78);
uniform float band_softness = 0.08;
uniform float grain = 0.06;
uniform float ground_shade = 0.12;
uniform vec3 tint : source_color = vec3(1.0);
uniform float flash = 0.0;

varying vec3 world_pos;

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
}

vec3 to_srgb(vec3 c) {
	return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), c));
}

void fragment() {
	// vertex colours are linear (glTF); the Compatibility renderer takes ALBEDO in sRGB
	vec3 c = (OUTPUT_IS_SRGB ? to_srgb(COLOR.rgb) : COLOR.rgb) * tint;
	float g = noise(world_pos * vec3(9.0, 2.5, 9.0)) * 0.6 + noise(world_pos * 31.0) * 0.4;
	c *= 1.0 - grain + grain * 2.0 * g;
	c *= mix(1.0 - ground_shade, 1.0, smoothstep(0.0, 0.45, world_pos.y));
	ALBEDO = mix(c, vec3(1.0, 0.95, 0.85), flash);
	ROUGHNESS = 1.0;
	SPECULAR = 0.0;
}

void light() {
	float ndl = dot(NORMAL, LIGHT);
	if (LIGHT_IS_DIRECTIONAL) {
		// the sun: two flat steps, and its cool tint in the shade
		float lit = smoothstep(0.0, band_softness, ndl) * 0.8 + smoothstep(0.45, 0.45 + band_softness, ndl) * 0.2;
		lit *= smoothstep(0.2, 0.6, ATTENUATION);
		DIFFUSE_LIGHT += mix(shade_tint * 0.5, vec3(1.0), lit) * LIGHT_COLOR / PI;
	} else {
		// fires and lamps: plain light that fades with distance
		DIFFUSE_LIGHT += clamp(ndl, 0.0, 1.0) * ATTENUATION * LIGHT_COLOR / PI;
	}
}
