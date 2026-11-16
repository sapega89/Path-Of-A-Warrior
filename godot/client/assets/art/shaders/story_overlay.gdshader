shader_type canvas_item;
// Over a story picture: slanting rain, the dark of the corners and the grain of paper.

uniform float rain = 0.0;
uniform vec3 rain_colour : source_color = vec3(0.8, 0.82, 0.9);
uniform float vignette = 0.5;
uniform vec3 vignette_colour : source_color = vec3(0.06, 0.05, 0.07);
uniform float aspect = 1.3;

float hash(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

void fragment() {
	vec2 uv = UV;
	float dark = smoothstep(0.42, 0.95, length((uv - 0.5) * vec2(1.0, 1.15) * 1.25)) * vignette;
	dark = clamp(dark + hash(floor(uv * vec2(aspect, 1.0) * 400.0)) * 0.05, 0.0, 1.0);
	vec2 q = vec2(uv.x * aspect * 110.0 + uv.y * 22.0, uv.y);
	float lane = floor(q.x);
	float h = hash(vec2(lane, 3.0));
	float drop = step(0.55, h) * (1.0 - smoothstep(0.06, 0.16, abs(fract(q.x) - 0.5)))
		* step(fract(uv.y * 2.2 + h * 13.0), 0.22 + 0.1 * h);
	float wet = drop * rain * (0.25 + 0.3 * h);
	float a = wet + dark * (1.0 - wet);
	vec3 c = (rain_colour * wet + vignette_colour * dark * (1.0 - wet)) / max(a, 0.0001);
	COLOR = vec4(c, a);
}
