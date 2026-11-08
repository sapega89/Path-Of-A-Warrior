// Shared by the effect shaders: how a quad or a cylinder of an effect turns to the camera,
// a little noise, and the palette's sRGB colours for the renderer in use.

// 0 as placed, 1 facing the camera, 2 upright and turned to the camera, 3 keeping its X axis
// (a bolt, a streak) and turned to the camera about it
uniform int billboard = 0;
// drawn this much closer to the camera, so that it shows over the figure it is on
uniform float toward = 0.0;

mat4 fx_modelview(mat4 model, mat4 view, mat4 inv_view) {
	vec3 sx = model[0].xyz;
	vec3 sy = model[1].xyz;
	vec3 sz = model[2].xyz;
	vec3 o = model[3].xyz;
	vec3 cam = inv_view[3].xyz;
	mat4 m = model;
	if (billboard == 1) {
		m = mat4(vec4(inv_view[0].xyz * length(sx), 0.0), vec4(inv_view[1].xyz * length(sy), 0.0),
			vec4(inv_view[2].xyz * length(sz), 0.0), vec4(o, 1.0));
	} else if (billboard == 2) {
		vec3 to_cam = cam - o;
		to_cam.y = 0.0;
		vec3 f = length(to_cam) > 0.0001 ? normalize(to_cam) : vec3(0.0, 0.0, 1.0);
		vec3 r = normalize(cross(vec3(0.0, 1.0, 0.0), f));
		m = mat4(vec4(r * length(sx), 0.0), vec4(0.0, length(sy), 0.0, 0.0), vec4(f * length(sz), 0.0),
			vec4(o, 1.0));
	} else if (billboard == 3) {
		vec3 axis = normalize(sx);
		vec3 side = cross(normalize(cam - o), axis);
		side = length(side) > 0.0001 ? normalize(side) : vec3(0.0, 1.0, 0.0);
		vec3 n = cross(axis, side);
		m = mat4(vec4(sx, 0.0), vec4(side * length(sy), 0.0), vec4(n * length(sz), 0.0), vec4(o, 1.0));
	}
	mat4 mv = view * m;
	if (toward != 0.0) {
		mv[3].xyz += normalize(-mv[3].xyz) * toward;
	}
	return mv;
}

float fx_hash(float n) {
	return fract(sin(n) * 43758.5453);
}

float fx_noise(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	f = f * f * (3.0 - 2.0 * f);
	float n = i.x + i.y * 57.0;
	return mix(mix(fx_hash(n), fx_hash(n + 1.0), f.x), mix(fx_hash(n + 57.0), fx_hash(n + 58.0), f.x), f.y);
}

// the palette is sRGB; a renderer that writes linear colour gets them converted
vec3 fx_colour(vec3 c, bool output_is_srgb) {
	return output_is_srgb ? c : pow(c, vec3(2.2));
}
