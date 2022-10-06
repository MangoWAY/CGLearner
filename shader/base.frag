#version 330 core
out vec4 color;
in vec3 c;
in vec2 uv;
uniform sampler2D ourTexture;
void main(){
    vec3 a = c;
    vec2 uv1 = vec2(uv.x,1.0-uv.y);
    color = texture(ourTexture, uv1);
}
