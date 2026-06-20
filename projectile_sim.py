import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def calculate_3d_trajectory(v0, pitch, yaw, drag):
    g, dt = 9.81, 0.01
    pitch_rad, yaw_rad = math.radians(pitch), math.radians(yaw)
    
    vz = v0 * math.sin(pitch_rad)
    v_ground = v0 * math.cos(pitch_rad)
    vx = v_ground * math.cos(yaw_rad)
    vy = v_ground * math.sin(yaw_rad)
    
    x, y, z = 0.0, 0.0, 0.0
    x_pts, y_pts, z_pts = [x], [y], [z]
    
    while z >= 0:
        speed = math.sqrt(vx**2 + vy**2 + vz**2)
        ax, ay, az = -drag*speed*vx, -drag*speed*vy, -g-(drag*speed*vz)
        vx += ax * dt; vy += ay * dt; vz += az * dt
        x += vx * dt; y += vy * dt; z += vz * dt
        if z >= 0:
            x_pts.append(x); y_pts.append(y); z_pts.append(z)
    return x_pts, y_pts, z_pts

# Cyberpunk UI Paint Scheme
fig = plt.figure(figsize=(10, 7), facecolor='#0b0f19')
ax = fig.add_subplot(111, projection='3d', facecolor='#0b0f19')
plt.subplots_adjust(bottom=0.35)

x, y, z = calculate_3d_trajectory(30, 45, 45, 0.01)
line, = ax.plot(x, y, z, lw=3, color='#00ffcc', label='Vector Flight Path')

# Dark Grid Architecture
ax.set_xlim(0, 60); ax.set_ylim(0, 60); ax.set_zlim(0, 30)
ax.xaxis.label.set_color('#8a99ad'); ax.yaxis.label.set_color('#8a99ad'); ax.zaxis.label.set_color('#8a99ad')
ax.tick_params(colors='#8a99ad')
ax.set_facecolor('#0b0f19')
ax.xaxis.set_pane_color((0.04, 0.06, 0.1, 1.0))
ax.yaxis.set_pane_color((0.04, 0.06, 0.1, 1.0))
ax.zaxis.set_pane_color((0.04, 0.06, 0.1, 1.0))
ax.set_title("ADVANCED BALLISTICS COMPUTATION MATRIX", color='#ffffff', fontsize=11, fontweight='bold', pad=20)

# Colored Sliders Matrix
slider_bg = '#161f30'
ax_v0 = plt.axes([0.15, 0.22, 0.65, 0.02], facecolor=slider_bg)
ax_pitch = plt.axes([0.15, 0.17, 0.65, 0.02], facecolor=slider_bg)
ax_yaw = plt.axes([0.15, 0.12, 0.65, 0.02], facecolor=slider_bg)
ax_drag = plt.axes([0.15, 0.07, 0.65, 0.02], facecolor=slider_bg)

s_v0 = Slider(ax_v0, 'VELOCITY', 10.0, 50.0, valinit=30, valfmt='%1.1f m/s', color='#ff0055')
s_pitch = Slider(ax_pitch, 'PITCH', 10.0, 90.0, valinit=45, valfmt='%1.0f Deg', color='#00ffcc')
s_yaw = Slider(ax_yaw, 'YAW', 0.0, 90.0, valinit=45, valfmt='%1.0f Deg', color='#ffaa00')
s_drag = Slider(ax_drag, 'DRAG', 0.00, 0.05, valinit=0.01, valfmt='%1.3f C_d', color='#9900ff')

for s in [s_v0, s_pitch, s_yaw, s_drag]:
    s.label.set_color('#ffffff')
    s.valtext.set_color('#ffffff')

def update(val):
    x_n, y_n, z_n = calculate_3d_trajectory(s_v0.val, s_pitch.val, s_yaw.val, s_drag.val)
    line.set_xdata(x_n); line.set_ydata(y_n); line.set_3d_properties(z_n)
    max_val = max(max(x_n), max(y_n), max(z_n), 10)
    ax.set_xlim(0, max_val * 1.1); ax.set_ylim(0, max_val * 1.1); ax.set_zlim(0, max_val * 0.6)
    fig.canvas.draw_idle()

s_v0.on_changed(update); s_pitch.on_changed(update); s_yaw.on_changed(update); s_drag.on_changed(update)
plt.show()