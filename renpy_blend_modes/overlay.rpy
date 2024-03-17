init python:
    CC_OVERLAY_NAME = "crosscouloir.overlay"

    _overlay_blend_mode = BlendMode(CC_OVERLAY_NAME)

    _overlay_blend_mode.vars = """
uniform float u_lod_bias;
uniform sampler2D tex0;
attribute vec2 a_tex_coord;
varying vec2 v_tex_coord;

uniform tex1 sampler2D;
"""
    _overlay_blend_mode.fragment_functions = """
float blendOverlay(float base, float blend) {
    return base<0.5?(2.0*base*blend):(1.0-2.0*(1.0-base)*(1.0-blend));
}

vec3 blendOverlay(vec3 base, vec3 blend) {
    return vec3(blendOverlay(base.r,blend.r),blendOverlay(base.g,blend.g),blendOverlay(base.b,blend.b));
}

vec3 blendOverlay(vec3 base, vec3 blend, float opacity) {
    return (blendOverlay(base, blend) * opacity + base * (1.0 - opacity));
}
"""
    _overlay_blend_mode.vertex_shader = """
v_tex_coord = a_tex_coord;
"""
    _overlay_blend_mode.fragment_shader = """
vec4 bgcolor = texture2D(tex0, v_tex_coord.st, u_lod_bias);
vec4 maskcolor = texture2D(tex1, v_tex_coord.st, u_lod_bias)
vec3 blended = blendScreen(bgcolor.xyz, maskcolor.xyz, maskcolor.w);
gl_FragColor = vec4(blended, bgcolor.w);
"""
    _overlay_blend_mode.register()

    def cc_overlay(base, tex, fit=True):
        return Model().child(base, fit=fit).texture(tex).shader(CC_OVERLAY_NAME)