shader_type spatial;
// A ring around a thing one can break (a barrel, a crate, a bush in the way), so that it reads
// at a glance apart from what only stands around. Two passes of it make the mark, as
// ArtKit.BREAKABLE_RINGS sets them: a dark ring outside and a light one inside it, that slowly
// goes from brass to near white and back. The light ring stands out on dark ground and dark wood,
// the dark one on light ground and light wood. The back faces are pushed out along the normal by a
// fixed number of pixels, as in outline.gdshader, and by whole pixels of the world at least, so
// the rings do not break up in pixel art. The dark ring is pushed a little away from the camera
// too, so the light one lies over it. The last pass, breakable_glow.gdshader, warms the thing's
// edges in the same pulse.
render_mode unshaded, cull_front, shadows_disabled;

// at the dimmest and at the brightest of the pulse
uniform vec4 color : source_color;
uniform vec4 peak : source_color;
uniform float pulse_seconds = 1.6;  // one glow and back
uniform float width_px;  // in a window 720 pixels high
uniform float min_pixels;  // pixels of the world at least
uniform float behind;  // metres away from the camera

void vertex() {
	vec4 view = MODELVIEW_MATRIX * vec4(VERTEX, 1.0);
	view.z -= behind;
	vec4 clip = PROJECTION_MATRIX * view;
	vec3 n = mat3(MODELVIEW_MATRIX) * NORMAL;
	vec2 dir = (PROJECTION_MATRIX * vec4(n, 0.0)).xy;
	float len = length(dir);
	if (len > 0.0001) {
		dir /= len;
	}
	float width = max(width_px * VIEWPORT_SIZE.y / 720.0, min_pixels);
	clip.xy += dir * width * 2.0 / VIEWPORT_SIZE * clip.w;
	POSITION = clip;
}

void fragment() {
	ALBEDO = mix(color.rgb, peak.rgb, 0.5 + 0.5 * sin(TIME * TAU / pulse_seconds));
}
