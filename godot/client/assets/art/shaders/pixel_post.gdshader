shader_type canvas_item;
// The world in pixel art (pixel_view.gd): its small picture blown up without smoothing, each of
// its pixels a square, and its colours held to a few steps, as a pixel artist's palette.
// The steps are taken in OKLab, where equal steps look equal: so many of lightness, and of the
// colour (its a and b) a fixed size. Between two steps a 4×4 ordered dither mixes the pixels,
// so a slope of light becomes a pattern instead of a band. The pattern is laid on the world's
// pixels, not the screen's.

// steps of lightness from black to white
uniform float light_steps = 18.0;
// the size of a step of colour (OKLab a and b)
uniform float colour_step = 0.03;
// how much the pattern mixes neighbouring steps (0: hard bands, 1: a full dither)
uniform float dither = 0.4;

const float BAYER[16] = float[16](
	0.0, 8.0, 2.0, 10.0,
	12.0, 4.0, 14.0, 6.0,
	3.0, 11.0, 1.0, 9.0,
	15.0, 7.0, 13.0, 5.0);

vec3 to_linear(vec3 c) {
	return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)), step(vec3(0.04045), c));
}

vec3 to_srgb(vec3 c) {
	return mix(c * 12.92, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055, step(vec3(0.0031308), c));
}

vec3 to_oklab(vec3 c) {
	float l = 0.4122214708 * c.r + 0.5363325363 * c.g + 0.0514459929 * c.b;
	float m = 0.2119034982 * c.r + 0.6806995451 * c.g + 0.1073969566 * c.b;
	float s = 0.0883024619 * c.r + 0.2817188376 * c.g + 0.6299787005 * c.b;
	l = pow(max(l, 0.0), 1.0 / 3.0);
	m = pow(max(m, 0.0), 1.0 / 3.0);
	s = pow(max(s, 0.0), 1.0 / 3.0);
	return vec3(
		0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
		1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
		0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s);
}

vec3 from_oklab(vec3 c) {
	float l = c.x + 0.3963377774 * c.y + 0.2158037573 * c.z;
	float m = c.x - 0.1055613458 * c.y - 0.0638541728 * c.z;
	float s = c.x - 0.0894841775 * c.y - 1.2914855480 * c.z;
	l = l * l * l;
	m = m * m * m;
	s = s * s * s;
	return vec3(
		4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
		-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
		-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s);
}

void fragment() {
	ivec2 size = textureSize(TEXTURE, 0);
	ivec2 cell = clamp(ivec2(floor(UV * vec2(size))), ivec2(0), size - 1);
	vec4 src = texelFetch(TEXTURE, cell, 0);
	vec3 lab = to_oklab(to_linear(src.rgb));
	float t = ((BAYER[(cell.x & 3) + (cell.y & 3) * 4] + 0.5) / 16.0 - 0.5) * dither;
	lab.x = floor(lab.x * light_steps + 0.5 + t) / light_steps;
	lab.yz = floor(lab.yz / colour_step + 0.5 + t) * colour_step;
	COLOR = vec4(to_srgb(clamp(from_oklab(lab), 0.0, 1.0)), src.a);
}
