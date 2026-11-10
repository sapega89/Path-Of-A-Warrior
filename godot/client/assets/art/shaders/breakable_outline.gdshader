shader_type spatial;
// The outline of a thing one can break (a barrel, a crate, a bush in the way): in place of the
// figures' ink, brass that slowly glows brighter and dims, so it reads apart from what only
// stands around. The back faces are pushed out along the normal by a fixed number of pixels,
// as in outline.gdshader. Its next pass, breakable_glow.gdshader, warms the thing's edges.
render_mode unshaded, cull_front, shadows_disabled;

uniform vec4 ink : source_color = vec4(0.169, 0.129, 0.11, 1.0);
uniform vec4 brass : source_color = vec4(1.0, 0.8, 0.4, 1.0);
uniform float width_px = 3.0;
uniform float pulse_seconds = 1.6;  // one glow and back
uniform float low = 0.55;  // how much brass at the dimmest

void vertex() {
	vec4 clip = PROJECTION_MATRIX * (MODELVIEW_MATRIX * vec4(VERTEX, 1.0));
	vec3 n = mat3(MODELVIEW_MATRIX) * NORMAL;
	vec2 dir = (PROJECTION_MATRIX * vec4(n, 0.0)).xy;
	float len = length(dir);
	if (len > 0.0001) {
		dir /= len;
	}
	float scale = VIEWPORT_SIZE.y / 720.0;
	clip.xy += dir * width_px * scale * 2.0 / VIEWPORT_SIZE * clip.w;
	POSITION = clip;
}

void fragment() {
	float glow = mix(low, 1.0, 0.5 + 0.5 * sin(TIME * TAU / pulse_seconds));
	ALBEDO = mix(ink.rgb, brass.rgb, glow);
}
