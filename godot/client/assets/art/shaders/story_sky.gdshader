shader_type canvas_item;
// The sky of a story picture, painted: from the colour at the top down to the colour at the
// horizon in brush strokes, the glow and the disc of the sun (or the moon), banks of cloud lit
// on the side of the sun, stars, and a bolt of lightning.

uniform vec3 top : source_color = vec3(0.2, 0.25, 0.4);
uniform vec3 horizon : source_color = vec3(0.85, 0.7, 0.5);
uniform float horizon_y = 0.62;  // where the sky meets the land, from the top
uniform vec3 glow : source_color = vec3(1.0, 0.8, 0.5);
uniform float glow_size = 0.35;
uniform vec2 sun = vec2(0.7, 0.55);
uniform float sun_size = 0.0;  // the disc's radius (0: none)
uniform vec3 sun_colour : source_color = vec3(1.0, 0.9, 0.6);
uniform float clouds = 0.4;  // how much of the sky they cover
uniform vec3 cloud_dark : source_color = vec3(0.3, 0.3, 0.4);
uniform vec3 cloud_lit : source_color = vec3(0.9, 0.75, 0.6);
uniform float stars = 0.0;
uniform float bolt = -1.0;  // the x of a bolt of lightning (none below 0)
uniform float seed = 0.0;
uniform float aspect = 1.3;

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

// cloud density at a point of the picture: long banks, flatter near the horizon
float density(vec2 uv) {
	vec2 p = vec2(uv.x * aspect * 2.0, uv.y * 5.5) + seed;
	float warp = fbm(p * 0.6 + 4.3);
	return fbm(p + vec2(warp * 1.6, warp * 0.4));
}

void fragment() {
	vec2 uv = UV;
	float h = clamp(uv.y / horizon_y, 0.0, 1.0);
	float strokes = noise(vec2(uv.x * aspect * 4.0, uv.y * 60.0) + seed) - 0.5;
	vec3 c = mix(top, horizon, smoothstep(0.0, 1.0, pow(h + strokes * 0.06, 1.4)));
	float r = length((uv - sun) * vec2(aspect, 1.0));
	c = mix(c, glow, exp(-r / max(glow_size, 0.001) * 2.2) * 0.85);
	float n = density(uv);
	float cover = smoothstep(1.0 - clouds, 1.0 - clouds + 0.16, n) * smoothstep(horizon_y + 0.02, horizon_y - 0.08, uv.y);
	vec2 towards = normalize(sun - uv + vec2(0.0001)) * 0.025;
	float lit = clamp((n - density(uv + towards)) * 9.0 + 0.35, 0.0, 1.0);
	vec3 cc = mix(cloud_dark, cloud_lit, clamp(lit * (0.35 + exp(-r * 1.6)), 0.0, 1.0));
	cc *= 0.94 + 0.12 * noise(vec2(uv.x * aspect * 30.0, uv.y * 90.0));
	float disc = (1.0 - smoothstep(sun_size, sun_size + 0.004, r)) * step(0.0001, sun_size);
	c = mix(c, sun_colour, disc);
	c = mix(c, cc, cover * 0.94);
	vec2 cell = floor(uv * vec2(aspect, 1.0) * 160.0);
	float star = step(0.988, hash(cell + seed)) * (0.4 + 0.6 * hash(cell + 3.7));
	c += vec3(star) * stars * (1.0 - cover) * (1.0 - h * h);
	if (bolt >= 0.0) {
		float x = bolt + (noise(vec2(uv.y * 7.0, seed)) - 0.5) * 0.16 + (noise(vec2(uv.y * 29.0, seed + 5.0)) - 0.5) * 0.04;
		float w = abs(uv.x - x) * aspect;
		float on = smoothstep(horizon_y, horizon_y - 0.06, uv.y) * smoothstep(0.0, 0.08, uv.y);
		c += vec3(0.55, 0.5, 0.95) * exp(-w * 28.0) * 0.55 * on;
		c = mix(c, vec3(0.97, 0.95, 1.0), (1.0 - smoothstep(0.0012, 0.0035, w)) * on);
	}
	COLOR = vec4(c, 1.0);
}
