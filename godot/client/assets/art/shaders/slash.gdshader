shader_type spatial;
// Sabre trail: a bright arc that fades along its length (UV.x) and over its life.
render_mode unshaded, blend_add, cull_disabled, depth_draw_never, shadows_disabled;

uniform vec4 color : source_color = vec4(1.0, 0.82, 0.48, 1.0);
uniform float life = 0.0;

void fragment() {
	float along = UV.x;
	float head = 1.0 - smoothstep(life * 1.4 - 0.15, life * 1.4 + 0.05, along);
	float tail = smoothstep(life * 1.4 - 0.75, life * 1.4 - 0.2, along);
	float edge = smoothstep(0.55, 0.9, UV.y) * (1.0 - smoothstep(0.92, 1.0, UV.y));
	float a = head * tail * edge * (1.0 - smoothstep(0.7, 1.0, life));
	ALBEDO = color.rgb * a;
	ALPHA = a * 0.85;
}
