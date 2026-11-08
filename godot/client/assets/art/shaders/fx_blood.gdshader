shader_type spatial;
// Blood of a hit in the new art: drops thrown out where the blow lands, stretched along their
// flight and falling (SPRAY, a quad turned to the camera), and the blots and drops they leave
// on the ground (SPLAT, a quad lying flat). Dark red, covering what is behind; colours are
// sRGB, like the palette. progress 0..1 runs the spray and spreads the blot.
render_mode unshaded, blend_mix, cull_disabled, depth_draw_never, shadows_disabled, fog_disabled;

#include "res://assets/art/shaders/fx_common.gdshaderinc"

const int SPRAY = 0;
const int SPLAT = 1;

uniform int shape = 0;
uniform vec3 color = vec3(0.66, 0.09, 0.07);
uniform vec3 dark = vec3(0.24, 0.02, 0.03);
uniform float progress = 0.0;
uniform float strength = 1.0;
uniform float seed = 0.0;
uniform float count = 14.0;
// the side the drops fly to (-1 left, 1 right of the quad; 0 both)
uniform float side = 0.0;

void vertex() {
	MODELVIEW_MATRIX = fx_modelview(MODEL_MATRIX, VIEW_MATRIX, INV_VIEW_MATRIX);
}

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	p.y = -p.y;
	float a = 0.0;
	float lit = 0.0;
	if (shape == SPRAY) {
		float t = progress;
		for (int i = 0; i < 24; i++) {
			if (float(i) >= count) {
				break;
			}
			float fi = float(i) + seed * 13.7;
			float ang = fx_hash(fi * 1.31) * 6.2832;
			vec2 dir = vec2(cos(ang), sin(ang) * 0.6 + 0.45);
			if (side != 0.0) {
				dir.x = (abs(dir.x) + 0.25) * side;
			}
			float speed = 0.8 + fx_hash(fi * 2.17) * 0.8;
			// thrown out and falling
			vec2 at = dir * speed * t + vec2(0.0, -1.3 * t * t);
			vec2 vel = dir * speed + vec2(0.0, -2.6 * t);
			float r = mix(0.085, 0.03, fx_hash(fi * 3.7)) * (1.0 - 0.4 * t);
			vec2 v = normalize(vel + vec2(0.0001));
			vec2 d = p - at;
			float along = dot(d, v);
			float across = dot(d, vec2(-v.y, v.x));
			float stretch = 1.0 + length(vel) * 1.4;
			float drop = smoothstep(1.0, 0.75, length(vec2(along / stretch, across)) / r);
			a = max(a, drop);
			lit = max(lit, drop * smoothstep(-0.2, 0.6, along / (r * stretch)));
		}
		// the burst where the blow lands, gone at once
		float burst = smoothstep(0.32, 0.05, length(p * vec2(1.0, 1.4))) * (1.0 - smoothstep(0.0, 0.3, t));
		a = max(a, burst);
	} else {
		// a blot with ragged edges and drops thrown round it
		float n = fx_noise(p * 3.2 + vec2(seed * 5.3, seed * 2.9));
		float grow = smoothstep(0.0, 0.35, progress);
		float blot = smoothstep(0.5, 0.36, length(p * vec2(1.0, 1.3)) / mix(0.4, 1.0, grow) + (n - 0.5) * 0.35);
		for (int i = 0; i < 9; i++) {
			float fi = float(i) + seed * 7.1;
			float ang = fx_hash(fi * 1.7) * 6.2832;
			vec2 c = vec2(cos(ang), sin(ang)) * (0.45 + fx_hash(fi * 2.9) * 0.45) * grow;
			blot = max(blot, smoothstep(1.0, 0.65, length(p - c) / mix(0.035, 0.09, fx_hash(fi * 4.3))));
		}
		a = blot * grow;
		lit = 0.35 + 0.4 * n;
	}
	ALBEDO = fx_colour(mix(dark, color, lit), OUTPUT_IS_SRGB);
	ALPHA = clamp(a * strength, 0.0, 1.0);
}
