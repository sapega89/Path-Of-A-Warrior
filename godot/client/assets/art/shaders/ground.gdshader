shader_type spatial;
// Steppe ground painted in the palette: soil, dry grass and green patches mixed by
// world-space noise, trodden paths from the vertex colour (r = path, g = green).

uniform vec3 soil : source_color = vec3(0.788, 0.631, 0.357);
uniform vec3 grass_dry : source_color = vec3(0.62, 0.604, 0.361);
uniform vec3 grass_green : source_color = vec3(0.435, 0.541, 0.29);
uniform vec3 path : source_color = vec3(0.72, 0.56, 0.33);
uniform vec3 path_dark : source_color = vec3(0.55, 0.41, 0.24);
uniform vec3 shade_tint : source_color = vec3(0.56, 0.6, 0.78);

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
	float n = fbm(p * 0.35);
	float strokes = noise(vec2(p.x * 2.4 + p.y * 0.9, p.y * 4.5));
	vec3 c = mix(soil, grass_dry, smoothstep(0.35, 0.65, n));
	c = mix(c, grass_green, clamp(COLOR.g * smoothstep(0.3, 0.7, fbm(p * 0.6 + 11.0)) * 1.3, 0.0, 1.0));
	vec3 pc = mix(path, path_dark, smoothstep(0.4, 0.8, fbm(p * 1.5)) * 0.6);
	c = mix(c, pc, smoothstep(0.25, 0.6, COLOR.r + (n - 0.5) * 0.3));
	c *= 0.95 + 0.08 * strokes;
	ALBEDO = c;
	ROUGHNESS = 1.0;
	SPECULAR = 0.0;
}

void light() {
	float ndl = dot(NORMAL, LIGHT);
	if (LIGHT_IS_DIRECTIONAL) {
		float lit = smoothstep(0.2, 0.6, ATTENUATION) * clamp(ndl * 2.0, 0.0, 1.0);
		DIFFUSE_LIGHT += mix(shade_tint * 0.5, vec3(1.0), lit) * LIGHT_COLOR / PI;
	} else {
		DIFFUSE_LIGHT += clamp(ndl, 0.0, 1.0) * ATTENUATION * LIGHT_COLOR / PI;
	}
}
