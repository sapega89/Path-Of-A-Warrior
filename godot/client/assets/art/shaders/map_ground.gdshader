shader_type spatial;
// The ground of a map in the new art. The colour of each place comes in the vertex colour
// (sRGB, mixed where kinds of ground meet) with painted noise and brush strokes over it, and
// the detail of its kind by weights (mixed the same way): UV.x stony ground (pebbles and
// cracks), UV.y boards (planks), UV2.x paving (cobbles), UV2.y the face of a cliff (its slope
// painted as rock). Steep faces get their own look by the vertex alpha: 0 dark rock in strata,
// 0.25 an earth bank, 0.5 stone in courses, 1 logs. Two-step light (warm sun, cool shade), as the
// figures.

uniform vec3 shade_tint : source_color = vec3(0.56, 0.6, 0.78);
// the colour rock faces lean to (sRGB)
uniform vec3 cliff = vec3(0.42, 0.41, 0.46);
// the colour earth banks lean to (sRGB)
uniform vec3 bank = vec3(0.42, 0.31, 0.2);

varying vec3 world_pos;
varying vec3 world_normal;
varying vec4 detail;

float hash(vec2 p) {
	return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 x) {
	vec2 i = floor(x);
	vec2 f = fract(x);
	f = f * f * (3.0 - 2.0 * f);
	return mix(mix(hash(i), hash(i + vec2(1, 0)), f.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), f.x), f.y);
}

float fbm(vec2 p) {
	return noise(p) * 0.55 + noise(p * 2.13 + 7.1) * 0.3 + noise(p * 4.7 + 3.3) * 0.15;
}

// Round pebbles scattered on a grid: 1 a light stone, -1 a dark pit, 0 bare ground.
float pebbles(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	float h = hash(i);
	vec2 centre = vec2(hash(i + 3.1), hash(i + 7.7)) * 0.5 + 0.25;
	float r = 0.1 + 0.16 * hash(i + 1.3);
	float inside = 1.0 - smoothstep(r - 0.05, r, length((f - centre) * vec2(1.0, 1.3)));
	return inside * (h > 0.45 ? 1.0 : -1.0) * step(0.4, fract(h * 7.0));
}

// A thin dark line where a noise field crosses its middle: cracks in stone.
float crack(vec2 p) {
	return 1.0 - smoothstep(0.0, 0.03, abs(noise(p) - 0.5));
}

void vertex() {
	world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	world_normal = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
	detail = vec4(UV, UV2);
}

void fragment() {
	vec2 p = world_pos.xz;
	vec3 base = COLOR.rgb;
	float n = fbm(p * 0.45);
	float strokes = noise(vec2(p.x * 2.4 + p.y * 0.9, p.y * 4.5));
	vec3 c = base * (0.86 + 0.24 * n) * (0.94 + 0.1 * strokes);
	float top = step(0.3, world_pos.y) * smoothstep(0.8, 0.9, world_normal.y) * (1.0 - detail.w);
	// stony ground: pebbles light and dark; on the top of a cliff, a few cracks
	if (detail.x > 0.01) {
		float stones = pebbles(p * 7.0) * 0.18 + pebbles(p * 13.0 + 5.0) * 0.1;
		float cracks = crack(p * 1.3 + 11.0) * smoothstep(0.55, 0.75, noise(p * 0.6 + 3.0));
		float rough = (1.0 + stones) * (1.0 - cracks * 0.3 * top);
		c *= mix(1.0, rough, detail.x);
	}
	// boards: planks along Z, staggered joints, grain
	if (detail.y > 0.01) {
		float u = p.x * 3.0;
		float row = floor(u);
		float v = p.y * 0.7 + hash(vec2(row, 1.0)) * 5.0;
		float seam = smoothstep(0.0, 0.07, fract(u)) * smoothstep(1.0, 0.93, fract(u));
		float joint = smoothstep(0.0, 0.025, fract(v)) * smoothstep(1.0, 0.985, fract(v));
		float grain = 0.9 + 0.1 * noise(vec2(fract(u) * 9.0 + row * 13.0, p.y * 1.3));
		float tone = 0.86 + 0.22 * hash(vec2(row, floor(v)));
		vec3 boards = base * tone * grain * mix(0.5, 1.0, seam * joint);
		c = mix(c, boards, detail.y);
	}
	// paving: cobbles in staggered rows, dark joints
	if (detail.z > 0.01) {
		vec2 q = p * vec2(3.0, 3.8);
		q.x += floor(q.y) * 0.5;
		vec2 f = fract(q);
		float edge = min(min(f.x, 1.0 - f.x) * 1.27, min(f.y, 1.0 - f.y));
		float stone = smoothstep(0.03, 0.1, edge);
		float tone = 0.82 + 0.3 * hash(floor(q));
		float dome = 0.94 + 0.12 * smoothstep(0.08, 0.4, edge);
		vec3 paving = base * mix(0.5, tone * dome, stone);
		c = mix(c, paving, detail.z);
	}
	float steep = max(1.0 - smoothstep(0.45, 0.8, world_normal.y), detail.w);
	if (steep > 0.0) {
		float y = world_pos.y;
		float along = abs(world_normal.x) > abs(world_normal.z) ? world_pos.z : world_pos.x;
		// up the face: the height, and on the long slope of a cliff's face its depth too
		float up = y * 9.0 - world_pos.z * 2.5 * detail.w;
		float bands = 0.82 + 0.26 * sin(up * 1.3 + noise(vec2(along * 2.0, up * 0.3)) * 4.0);
		float splits = 1.0 - 0.4 * crack(vec2(along * 3.0, up * 0.15));
		float rough = 0.8 + 0.4 * fbm(vec2(along * 3.0, up * 0.6));
		vec3 rock = mix(base, cliff, 0.35) * bands * splits * rough;
		vec3 earth = mix(base * 0.6, bank, 0.55) * (0.85 + 0.15 * noise(vec2(along * 4.0, y * 9.0)));
		float course = fract(y * 3.2);
		float brick = fract(along * 2.2 + floor(y * 3.2) * 0.5);
		float joints = smoothstep(0.0, 0.07, course) * smoothstep(1.0, 0.93, course)
			* smoothstep(0.0, 0.05, brick) * smoothstep(1.0, 0.95, brick);
		vec3 masonry = base * 0.74 * mix(0.55, 0.9 + 0.2 * hash(floor(vec2(along * 2.2 + floor(y * 3.2) * 0.5, y * 3.2))), joints);
		vec3 logs = base * 0.8 * (0.62 + 0.38 * sin(fract(y * 3.6) * PI));
		float style = COLOR.a;
		vec3 facec = style < 0.15 ? rock : (style < 0.4 ? earth : (style < 0.75 ? masonry : logs));
		c = mix(c, facec, steep);
	}
	ALBEDO = OUTPUT_IS_SRGB ? c : pow(c, vec3(2.2));
	ROUGHNESS = 1.0;
	SPECULAR = 0.0;
}

void light() {
	float ndl = dot(NORMAL, LIGHT);
	if (LIGHT_IS_DIRECTIONAL) {
		float lit = smoothstep(0.2, 0.6, ATTENUATION) * clamp(ndl * 2.0, 0.0, 1.0);
		DIFFUSE_LIGHT += mix(shade_tint * 0.5, vec3(1.0), lit) * LIGHT_COLOR / PI;
	} else {
		DIFFUSE_LIGHT += clamp(ndl, 0.0, 1.0) * ATTENUATION * LIGHT_COLOR / PI;
	}
}
