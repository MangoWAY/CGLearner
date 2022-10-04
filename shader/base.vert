#version 330 core
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aNormal;
layout(location = 2) in vec3 aColor;
out vec3 n;
out vec3 c;
out vec3 FragPos;
uniform mat4 u_mvp;
void main(){
    gl_Position.xyz = aPos;
    gl_Position.w = 1.0;
    gl_Position = u_mvp * gl_Position;
    c = aColor;
}
