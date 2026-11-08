shader_type spatial;
// Dust and smoke of the effects in the new art: a soft cloud in two tones (lit above, in
// shade below), like the painted figures. Colours are sRGB, like the palette.
render_mode unshaded, blend_mix, cull_disabled, depth_draw_never, shadows_disabled, fog_disabled;

#include "res://assets/art/shaders/fx_common.gdshaderinc"

uniform vec3 color = vec3(0.86, 0.78, 0.6);
uniform vec3 shade = vec3(0.62, 0.56, 0.5);
uniform float strength = 1.0;
uniform float seed = 0.0;

void vertex() {
	MODELVIEW_MATRIX = fx_modelview(MODEL_MATRIX, VIEW_MATRIX, INV_VIEW_MATRIX);
}

void fragment() {
	vec2 p = UV * 2.0 - 1.0;
	float n = fx_noise(UV * 3.0 + vec2(seed * 3.1, seed * 1.7));
	float a = smoothstep(1.0, 0.35, length(p) + (n - 0.5) * 0.5);
	float lit = step(0.0, -p.y + (n - 0.5) * 0.5);
	ALBEDO = fx_colour(mix(shade, color, lit), OUTPUT_IS_SRGB);
	ALPHA = clamp(a * strength, 0.0, 1.0);
}
