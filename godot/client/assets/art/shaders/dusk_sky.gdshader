shader_type sky;
// The sky over a 3D place in the new art, painted like the story pictures' sky
// (story_sky.gdshader): from the colour at the top down to the colour at the horizon in brush
// strokes, a glow where the hidden sun or moon is, low banks of cloud lit on its side. Below the
// horizon it stays the horizon's colour, the fog of the land fades into it. Colours are sRGB.

uniform vec3 top : source_color = vec3(0.07, 0.08, 0.11);
uniform vec3 horizon : source_color = vec3(0.29, 0.28, 0.35);
uniform vec3 glow : source_color = vec3(0.42, 0.34, 0.44);
uniform float glow_size = 0.35;
uniform vec3 glow_dir = vec3(0.6, 0.12, -0.8);  // where the glow is, from the viewer
uniform float clouds = 0.62;  // how much of the sky they cover
uniform vec3 cloud_dark : source_color = vec3(0.11, 0.12, 0.16);
uniform vec3 cloud_lit : source_color = vec3(0.36, 0.38, 0.47);
uniform float seed = 11.0;

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
	float v = 0.0;
	float a = 0.5;
	for (int i = 0; i < 5; i++) {
		v += a * noise(p);
		p = p * 2.07 + vec2(1.7, 9.2);
		a *= 0.5;
	}
	return v;
}

// cloud density on the cloud layer, seen along a direction: long banks drawn out sideways
float density(vec3 d) {
	vec2 p = d.xz / (d.y + 0.12) * vec2(0.55, 1.4) + seed;
	float warp = fbm(p * 0.6 + 4.3);
	return fbm(p + vec2(warp * 1.6, warp * 0.4));
}

void sky() {
	vec3 d = normalize(EYEDIR);
	float up = clamp(d.y, 0.0, 1.0);
	float strokes = noise(vec2(atan(d.x, d.z) * 9.0, up * 60.0) + seed) - 0.5;
	vec3 c = mix(horizon, top, smoothstep(0.0, 1.0, pow(up + strokes * 0.03, 0.6)));
	vec3 g = normalize(glow_dir);
	float r = acos(clamp(dot(d, g), -1.0, 1.0));
	c = mix(c, glow, exp(-r / max(glow_size, 0.001) * 2.2) * 0.85);
	float n = density(d);
	float cover = smoothstep(1.0 - clouds, 1.0 - clouds + 0.16, n) * smoothstep(0.0, 0.08, d.y);
	vec3 towards = normalize(g - d * dot(g, d) + vec3(0.0, 0.0001, 0.0)) * 0.03;
	float lit = clamp((n - density(normalize(d + towards))) * 9.0 + 0.35, 0.0, 1.0);
	vec3 cc = mix(cloud_dark, cloud_lit, clamp(lit * (0.35 + exp(-r * 1.6)), 0.0, 1.0));
	c = mix(c, cc, cover * 0.94);
	COLOR = c;
}
