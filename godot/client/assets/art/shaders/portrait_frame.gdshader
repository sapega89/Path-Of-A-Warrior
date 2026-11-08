shader_type canvas_item;
// The frame of a portrait or a story picture: hard corners, an iron rim (worn light at the top,
// dark below) with a thin ink line inside it, and the picture darker towards the rim.
// In fractions of the picture's height, so a frame looks the same at any size.

uniform vec3 rim_light : source_color = vec3(0.56, 0.54, 0.5);
uniform vec3 rim_dark : source_color = vec3(0.2, 0.19, 0.18);
uniform vec3 ink : source_color = vec3(0.059, 0.051, 0.047);
uniform float radius = 0.025;
uniform float width = 0.032;
// the picture's width over its height
uniform float aspect = 1.0;

// distance to the edge of a rounded rectangle of half sides b (negative inside)
float rounded(vec2 p, vec2 b, float r) {
	vec2 q = abs(p) - (b - r);
	return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
}

void fragment() {
	float d = rounded((UV - 0.5) * vec2(aspect, 1.0), vec2(aspect * 0.5, 0.5), radius);
	float aa = max(fwidth(d), 0.0005);
	vec4 c = COLOR;
	c.rgb *= 1.0 - 0.32 * smoothstep(-width - 0.16, -width, d);
	float line = 1.0 - smoothstep(0.0, aa * 1.5, abs(d + width + aa));
	c.rgb = mix(c.rgb, ink, line);
	float on_rim = smoothstep(-width - aa, -width + aa, d);
	vec3 iron = mix(rim_light, rim_dark, smoothstep(0.0, 1.0, UV.y));
	c.rgb = mix(c.rgb, iron, on_rim);
	c.a *= 1.0 - smoothstep(-aa, aa, d);
	COLOR = c;
}
