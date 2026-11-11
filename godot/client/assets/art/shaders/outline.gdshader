shader_type spatial;
// Ink outline around living figures: the back faces are pushed out along the normal by a fixed
// number of pixels (MIN_PIXELS of the world at least, so it does not break up in pixel art) and
// drawn in one dark colour.
render_mode unshaded, cull_front, shadows_disabled;

uniform vec4 ink : source_color = vec4(0.169, 0.129, 0.11, 1.0);
uniform float width_px = 1.6;
// pixels of the world at least
const float MIN_PIXELS = 1.25;

void vertex() {
	vec4 clip = PROJECTION_MATRIX * (MODELVIEW_MATRIX * vec4(VERTEX, 1.0));
	vec3 n = mat3(MODELVIEW_MATRIX) * NORMAL;
	vec2 dir = (PROJECTION_MATRIX * vec4(n, 0.0)).xy;
	float len = length(dir);
	if (len > 0.0001) {
		dir /= len;
	}
	float width = max(width_px * VIEWPORT_SIZE.y / 720.0, MIN_PIXELS);
	clip.xy += dir * width * 2.0 / VIEWPORT_SIZE * clip.w;
	POSITION = clip;
}

void fragment() {
	ALBEDO = ink.rgb;
}
