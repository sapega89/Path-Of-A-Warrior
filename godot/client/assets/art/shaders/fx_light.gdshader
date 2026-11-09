shader_type spatial;
// The light of an effect in the new art (a blow, fire, lightning, a blessing): a shape drawn
// on a quad or on an open cylinder. Its glow is added to the picture; `body` makes its brightest
// part cover what is behind (fire, water and steel read on a bright steppe too). Each effect
// sets the shape, its colours (sRGB, like the palette) and how far it has gone (progress).
render_mode unshaded, blend_premul_alpha, cull_disabled, depth_draw_never, shadows_disabled, fog_disabled;

#include "res://assets/art/shaders/fx_common.gdshaderinc"

// shapes on a quad
const int GLOW = 0;    // a soft round light
const int RING = 1;    // a ring (with spikes when count > 0)
const int STAR = 2;    // rays out of a hot middle
const int FLAME = 3;   // a tongue of fire, the quad's bottom at its foot
const int BOLT = 4;    // a jagged line of lightning along UV.x
const int STREAK = 5;  // a tail of light, its head at UV.x = 1
const int RIBBON = 6;  // a body of fire along UV.x, the head at 1 (a ribbon mesh)
// shapes on an open cylinder (UV.x around it)
const int SPIRAL = 7;  // bands of light winding up
const int COLUMN = 8;  // a pillar of light in stripes
const int MOTES = 9;   // sparks of light rising
const int SPLASH = 10; // a wall of water with a jagged crest
// shapes on a ribbon mesh (UV.x along it, UV.y across: 0 inside, 1 outside)
const int SWEEP = 11;  // the trail of a blade, its head at progress

uniform vec3 core = vec3(1.0, 0.95, 0.8);
uniform vec3 edge = vec3(0.83, 0.65, 0.27);
uniform int shape = 0;
uniform float progress = 0.0;
uniform float strength = 1.0;
uniform float seed = 0.0;
uniform float count = 8.0;
uniform float radius = 0.7;
uniform float width = 0.12;
// 0: only light added; 1: the shape covers what is behind it where it is brightest
uniform float body = 0.0;

void vertex() {
	MODELVIEW_MATRIX = fx_modelview(MODEL_MATRIX, VIEW_MATRIX, INV_VIEW_MATRIX);
}

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	float r = length(p);
	float h = 1.0 - UV.y;
	float a = 0.0;
	float hot = 0.0;
	if (shape == GLOW) {
		float k = clamp(1.0 - r, 0.0, 1.0);
		a = k * k;
		hot = k * k * k;
	} else if (shape == RING) {
		float ang = atan(p.y, p.x);
		float rr = radius;
		if (count > 0.0) {
			rr += 0.12 * pow(abs(sin(ang * count * 0.5 + seed)), 6.0) * (0.5 + fx_hash(floor((ang + PI) / TAU * count) + seed));
		}
		float d = abs(r - rr);
		a = smoothstep(width, 0.0, d) + 0.18 * step(r, rr) * (r / max(rr, 0.001));
		hot = smoothstep(width * 0.5, 0.0, d);
	} else if (shape == STAR) {
		float ang = atan(p.y, p.x) + seed;
		float s = (ang + PI) / TAU * count;
		float len = mix(0.45, 1.0, fx_hash(floor(s) + seed * 7.0));
		float across = abs(fract(s) - 0.5);
		float ray = smoothstep((1.0 - r / len) * 0.3, 0.0, across) * step(r, len);
		float mid = pow(max(1.0 - r * 2.6, 0.0), 2.0);
		a = max(ray, mid);
		hot = max(mid, ray * (1.0 - r));
	} else if (shape == FLAME) {
		float sway = (fx_noise(vec2(h * 3.0 - TIME * 4.0, seed)) - 0.5) * 0.4 * h;
		float x = p.x - sway;
		float w = 0.85 * (1.0 - 0.55 * h);
		// tongues of different heights side by side, flickering
		float top = 0.4 + 0.6 * fx_noise(vec2(x * 3.5 + seed, TIME * 2.5));
		float n = fx_noise(vec2(p.x * 4.0, h * 5.0 - TIME * 6.0 + seed));
		a = smoothstep(w, w * 0.2, abs(x)) * smoothstep(top, top - 0.3, h + (n - 0.5) * 0.25) * smoothstep(0.0, 0.05, h);
		hot = smoothstep(0.55, 0.0, abs(x)) * smoothstep(top, 0.0, h);
	} else if (shape == BOLT) {
		float x = UV.x;
		float flick = floor(TIME * 14.0 + seed * 3.0);
		float n = x * 9.0;
		float i = floor(n);
		float f = fract(n);
		float o1 = (fx_hash(i * 13.1 + seed * 71.0 + flick * 3.7) - 0.5) * 0.7;
		float o2 = (fx_hash((i + 1.0) * 13.1 + seed * 71.0 + flick * 3.7) - 0.5) * 0.7;
		float taper = sin(x * PI);
		float o = mix(o1, o2, f) * taper;
		float d = abs(p.y - o);
		float b1 = (fx_hash(i * 5.3 + seed * 11.0 + flick) - 0.5) * 0.9;
		float b2 = (fx_hash((i + 1.0) * 5.3 + seed * 11.0 + flick) - 0.5) * 0.9;
		float d2 = abs(p.y - mix(b1, b2, f) * taper);
		a = smoothstep(0.07, 0.0, d) + 0.5 * exp(-d * 6.0) + 0.45 * smoothstep(0.04, 0.0, d2);
		hot = smoothstep(0.05, 0.0, d);
	} else if (shape == STREAK) {
		float x = UV.x;
		float w = mix(0.04, 0.6, pow(x, 1.5));
		a = smoothstep(w, 0.0, abs(p.y)) * pow(x, 1.4) * (0.75 + 0.25 * fx_noise(vec2(x * 8.0 - TIME * 10.0, p.y * 3.0 + seed)));
		hot = a * x;
	} else if (shape == RIBBON) {
		float x = UV.x;
		float w = mix(0.25, 1.0, smoothstep(0.0, 0.85, x)) * (1.0 - 0.5 * smoothstep(0.94, 1.0, x));
		float n = fx_noise(vec2(x * 18.0 - TIME * 6.0, p.y * 2.0 + seed));
		float flesh = smoothstep(w, w * 0.25, abs(p.y) + n * 0.3);
		a = flesh * (0.8 + 0.2 * sin(x * 90.0 - TIME * 8.0)) * smoothstep(0.0, 0.3, x);
		hot = smoothstep(w * 0.5, 0.0, abs(p.y)) * x;
	} else if (shape == SPIRAL) {
		float s = fract(UV.x * count + h * 1.3 - TIME * 0.7 - progress);
		float band = smoothstep(0.0, 0.08, s) * smoothstep(0.42, 0.12, s);
		float sparkle = step(0.93, fx_hash(floor(UV.x * 40.0) + floor(h * 20.0 - TIME * 6.0) * 40.0 + seed));
		a = (band * 0.85 + sparkle * 0.8) * smoothstep(0.0, 0.15, h) * smoothstep(1.0, 0.45, h);
		hot = band * 0.3 + sparkle;
	} else if (shape == COLUMN) {
		float stripes = pow(abs(sin((UV.x * count + seed) * PI)), 3.0);
		float n = fx_noise(vec2(UV.x * count * 2.0, h * 3.0 - TIME * 3.0));
		a = (0.25 + 0.75 * stripes * n) * smoothstep(1.0, 0.3, h) * smoothstep(0.0, 0.08, h);
		hot = stripes * n * (1.0 - h);
	} else if (shape == MOTES) {
		vec2 g = vec2(UV.x * count, h * 5.0 - TIME * 1.2 + seed);
		vec2 c = floor(g);
		float rnd = fx_hash(c.x * 7.3 + c.y * 91.1 + seed);
		vec2 off = vec2(rnd - 0.5, fract(rnd * 7.0) - 0.5) * 0.5;
		float dot_ = smoothstep(0.3, 0.05, length(fract(g) - 0.5 - off)) * step(0.45, rnd);
		a = dot_ * smoothstep(1.0, 0.4, h);
		hot = dot_;
	} else if (shape == SWEEP) {
		float lead = progress * 1.4;
		float head = 1.0 - smoothstep(lead - 0.15, lead + 0.05, UV.x);
		float tail = smoothstep(lead - 0.75, lead - 0.2, UV.x);
		float rim = smoothstep(0.45, 0.9, UV.y) * (1.0 - smoothstep(0.93, 1.0, UV.y));
		a = head * tail * rim * (1.0 - smoothstep(0.75, 1.0, progress));
		hot = smoothstep(0.75, 0.95, UV.y) * head;
	} else if (shape == SPLASH) {
		float top = 0.35 + 0.65 * fx_hash(floor(UV.x * count) + seed);
		a = smoothstep(top, top - 0.18, h) * (0.35 + 0.65 * h);
		hot = smoothstep(top - 0.25, top, h);
	}
	a = clamp(a * strength, 0.0, 1.0);
	ALBEDO = fx_colour(mix(edge, core, clamp(hot, 0.0, 1.0)), OUTPUT_IS_SRGB) * a;
	ALPHA = a * body;
}
