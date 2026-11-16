shader_type spatial;
// The warm edges of a thing one can break: brass light added where its surface turns away
// from the camera, a little over all of it, glowing and dimming with its outline
// (breakable_outline.gdshader).
render_mode unshaded, blend_add, depth_draw_never, shadows_disabled;

uniform vec4 brass : source_color = vec4(1.0, 0.8, 0.4, 1.0);
uniform float strength = 0.5;
uniform float pulse_seconds = 1.6;
uniform float low = 0.3;

void fragment() {
	float glow = mix(low, 1.0, 0.5 + 0.5 * sin(TIME * TAU / pulse_seconds));
	float edge = pow(1.0 - clamp(dot(NORMAL, VIEW), 0.0, 1.0), 2.0);
	ALBEDO = brass.rgb * (0.12 + edge) * glow * strength;
}
