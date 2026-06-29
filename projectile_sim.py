import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def calculate_3d_trajectory(v0, pitch, yaw, drag, mass):
    g, dt = 9.81, 0.01
    pitch_rad, yaw_rad = math.radians(pitch), math.radians(yaw)
    
    # Velocity Vector Components
    vz = v0 * math.sin(pitch_rad)
    v_ground = v0 * math.cos(pitch_rad)
    vx = v_ground * math.cos(yaw_rad)
    vy = v_ground * math.sin(yaw_rad)
    
    x, y, z = 0.0, 0.0, 0.0
    x_pts, y_pts, z_pts = [x], [y], [z]
    
    max_z = 0.0
    time_elapsed = 0.0
    
    while z >= 0:
        speed = math.sqrt(vx**2 + vy**2 + vz**2)
        
        # Drag Force F = -drag * speed * velocity_vector
        # Acceleration a = F / mass
        # Gravity only affects the Z axis (az = -g + drag_z/mass)
        ax = -(drag * speed * vx) / mass
        ay = -(drag * speed * vy) / mass
        az = -g - (drag * speed * vz) / mass
        
        vx += ax * dt; vy += ay * dt; vz += az * dt
        x += vx * dt; y += vy * dt; z += vz * dt
        time_elapsed += dt
        
        if z >= 0:
            x_pts.append(x); y_pts.append(y); z_pts.append(z)
            if z > max_z:
                max_z = z
                
    total_range = math.sqrt(x**2 + y**2)
    return x_pts, y_pts, z_pts, max_z, total_range, time_elapsed

# Cyberpunk UI Paint Scheme
fig = plt.figure(figsize=(12, 8), facecolor='#0b0f19')
ax = fig.add_subplot(111, projection='3d', facecolor='#0b0f19')
plt.subplots_adjust(bottom=0.38, left=0.1, right=0.9)

# Initial Calculation
x, y, z, max_height, final_range, flight_time = calculate_3d_trajectory(30, 45, 45, 0.01, 1.0)
line, = ax.plot(x, y, z, lw=3, color='#00ffcc', label='Vector Flight Path')

# Live HUD Analytics Text Box
hud_text = (f"=== REAL-TIME TELEMETRY ===\n"
            f"MAX ALTITUDE : {max_height:.2f} m\n"
            f"TOTAL RANGE  : {final_range:.2f} m\n"
            f"FLIGHT TIME  : {flight_time:.2f} s")
telemetry_box = fig.text(0.1, 0.82, hud_text, color='#00ffcc', fontsize=10, 
                         fontfamily='monospace', fontweight='bold',
                         bbox=dict(facecolor='#161f30', edgecolor='#ff0055', alpha=0.8, boxstyle='round,pad=0.5'))

# Dark Grid Architecture
max_val = max(max(x), max(y), max(z), 10)
ax.set_xlim(0, max_val * 1.1); ax.set_ylim(0, max_val * 1.1); ax.set_zlim(0, max_val * 0.6)
ax.xaxis.label.set_color('#8a99ad'); ax.yaxis.label.set_color('#8a99ad'); ax.zaxis.label.set_color('#8a99ad')
ax.tick_params(colors='#8a99ad')
ax.xaxis.set_pane_color((0.04, 0.06, 0.1, 1.0))
ax.yaxis.set_pane_color((0.04, 0.06, 0.1, 1.0))
ax.zaxis.set_pane_color((0.04, 0.06, 0.1, 1.0))
ax.set_title("QUANTUM BALLISTICS TELEMETRY MATRIX v2.0", color='#ffffff', fontsize=13, fontweight='bold', pad=30)

# Colored Sliders Matrix
slider_bg = '#161f30'
ax_v0 = plt.axes([0.15, 0.26, 0.65, 0.02], facecolor=slider_bg)
ax_pitch = plt.axes([0.15, 0.21, 0.65, 0.02], facecolor=slider_bg)
ax_yaw = plt.axes([0.15, 0.16, 0.65, 0.02], facecolor=slider_bg)
ax_drag = plt.axes([0.15, 0.11, 0.65, 0.02], facecolor=slider_bg)
ax_mass = plt.axes([0.15, 0.06, 0.65, 0.02], facecolor=slider_bg)

s_v0 = Slider(ax_v0, 'VELOCITY', 10.0, 60.0, valinit=30, valfmt='%1.1f m/s', color='#ff0055')
s_pitch = Slider(ax_pitch, 'PITCH', 5.0, 90.0, valinit=45, valfmt='%1.0f Deg', color='#00ffcc')
s_yaw = Slider(ax_yaw, 'YAW', 0.0, 90.0, valinit=45, valfmt='%1.0f Deg', color='#ffaa00')
s_drag = Slider(ax_drag, 'DRAG (Cd)', 0.00, 0.10, valinit=0.01, valfmt='%1.3f', color='#9900ff')
s_mass = Slider(ax_mass, 'MASS (Kg)', 0.1, 10.0, valinit=1.0, valfmt='%1.1f kg', color='#00ff00')

for s in [s_v0, s_pitch, s_yaw, s_drag, s_mass]:
    s.label.set_color('#ffffff')
    s.valtext.set_color('#ffffff')
    s.label.set_fontweight('bold')

def update(val):
    # Recalculate with Mass included
    x_n, y_n, z_n, m_z, f_r, f_t = calculate_3d_trajectory(s_v0.val, s_pitch.val, s_yaw.val, s_drag.val, s_mass.val)
    
    # Update Vector Path
    line.set_xdata(x_n); line.set_ydata(y_n); line.set_3d_properties(z_n)
    
    # Dynamic View Rescaling
    curr_max = max(max(x_n), max(y_n), max(z_n), 10)
    ax.set_xlim(0, curr_max * 1.1); ax.set_ylim(0, curr_max * 1.1); ax.set_zlim(0, curr_max * 0.7)
    
    # Dynamic Telemetry Update
    updated_text = (f"=== REAL-TIME TELEMETRY ===\n"
                    f"MAX ALTITUDE : {m_z:.2f} m\n"
                    f"TOTAL RANGE  : {f_r:.2f} m\n"
                    f"FLIGHT TIME  : {f_t:.2f} s")
    telemetry_box.set_text(updated_text)
    
    fig.canvas.draw_idle()

# Connect triggers
s_v0.on_changed(update); s_pitch.on_changed(update); s_yaw.on_changed(update); s_drag.on_changed(update); s_mass.on_changed(update)

plt.show()
