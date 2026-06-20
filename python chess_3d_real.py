import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

class CyberChess3D:
    def __init__(self):
        # Establish the base data matrix (Piece Type, Color)
        # Colors: 'C' = Cyan (Player 1), 'F' = Fuchsia (Player 2)
        self.board = {}
        self.setup_pieces()

        # Initialize Cyberpunk UI
        self.fig = plt.figure(figsize=(11, 9), facecolor='#05070a')
        self.ax = self.fig.add_subplot(111, projection='3d', facecolor='#05070a')
        plt.subplots_adjust(bottom=0.3) # Space for control console
        
        self.dynamic_artists = []
        self.render_board_base()
        self.update_visuals()

    def setup_pieces(self):
        """Initializes all 32 pieces at their standard backline coordinates."""
        backline = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        # Player 1 (Cyan)
        for x, p in enumerate(backline):
            self.board[(x, 0)] = (p, 'C')
            self.board[(x, 1)] = ('P', 'C')
        # Player 2 (Fuchsia)
        for x, p in enumerate(backline):
            self.board[(x, 7)] = (p, 'F')
            self.board[(x, 6)] = ('P', 'F')

    def draw_wireframe_piece(self, x, y, p_type, color_hex):
        """Generates distinctive 3D holographic wireframes per piece type."""
        artists = []
        cx, cy = x + 0.5, y + 0.5
        
        if p_type == 'P': # Pawn: Simple Low Pyramid
            z_top = 0.6
            corners = [[x+0.3, y+0.3, 0], [x+0.7, y+0.3, 0], [x+0.7, y+0.7, 0], [x+0.3, y+0.7, 0]]
            for c in corners:
                l, = self.ax.plot([c[0], cx], [c[1], cy], [c[2], z_top], color=color_hex, lw=1.5)
                artists.append(l)
        elif p_type == 'R': # Rook: Heavy Block Cylinder
            z_height = 0.9
            for hz in [0, z_height]:
                theta = np.linspace(0, 2*np.pi, 5)
                rx, ry = cx + 0.25*np.cos(theta), cy + 0.25*np.sin(theta)
                l, = self.ax.plot(rx, ry, hz, color=color_hex, lw=2)
                artists.append(l)
                if hz == 0:
                    for k in range(4):
                        v_line, = self.ax.plot([rx[k], rx[k]], [ry[k], ry[k]], [0, z_height], color=color_hex, lw=1.5)
                        artists.append(v_line)
        elif p_type == 'N': # Knight: Forward Spike (L-shape simulation)
            l, = self.ax.plot([cx-0.2, cx, cx+0.2], [cy-0.2, cy+0.2, cy], [0, 0.9, 0.4], color=color_hex, lw=2)
            artists.append(l)
        elif p_type == 'B': # Bishop: Sharp Diamond Pillar
            l, = self.ax.plot([cx, cx, cx, cx, cx], [cy-0.2, cy+0.2, cy, cy, cy-0.2], [0, 0, 1.1, 0, 0], color=color_hex, lw=2)
            artists.append(l)
            l2, = self.ax.plot([cx-0.2, cx+0.2, cx, cx, cx-0.2], [cy, cy, cy, cy, cy], [0, 0, 1.1, 0, 0], color=color_hex, lw=2)
            artists.append(l2)
        elif p_type == 'Q': # Queen: High Spired Canopy
            z_top = 1.4
            for r_val in [0.15, 0.35]:
                theta = np.linspace(0, 2*np.pi, 7)
                qx, qy = cx + r_val*np.cos(theta), cy + r_val*np.sin(theta)
                l, = self.ax.plot(qx, qy, 0 if r_val==0.35 else 0.7, color=color_hex, lw=1.5)
                artists.append(l)
            l_tip, = self.ax.plot([cx, cx], [cy, cy], [0, z_top], color=color_hex, lw=2.5)
            artists.append(l_tip)
        elif p_type == 'K': # King: Domed Crown with Cross
            z_top = 1.5
            theta = np.linspace(0, 2*np.pi, 9)
            kx, ky = cx + 0.3*np.cos(theta), cy + 0.3*np.sin(theta)
            l, = self.ax.plot(kx, ky, 0, color=color_hex, lw=2)
            artists.append(l)
            for theta_val in [0, np.pi/2, np.pi, 3*np.pi/2]:
                kx_s, ky_s = cx + 0.3*np.cos(theta_val), cy + 0.3*np.sin(theta_val)
                arc, = self.ax.plot([kx_s, cx, cx], [ky_s, cy, cy], [0, 1.2, z_top], color=color_hex, lw=2)
                artists.append(arc)
                
        return artists

    def render_board_base(self):
        """Draws the invariant background 8x8 matrix grid."""
        for i in range(8):
            for j in range(8):
                tile_color = '#0f172a' if (i + j) % 2 == 0 else '#060b14'
                X, Y = np.meshgrid([i, i+1], [j, j+1])
                self.ax.plot_surface(X, Y, np.zeros_like(X), color=tile_color, edgecolor='#1e293b', alpha=0.8)

    def update_visuals(self):
        """Wipes active frame artists and re-draws the board state from scratch."""
        for artist in self.dynamic_artists:
            try: artist.remove()
            except: pass
        self.dynamic_artists.clear()

        # Iterate and render current active coordinates
        for (x, y), (p_type, side) in self.board.items():
            color_hex = '#00ffcc' if side == 'C' else '#ff0055'
            piece_artists = self.draw_wireframe_piece(x, y, p_type, color_hex)
            self.dynamic_artists.extend(piece_artists)

        # Re-verify layout bounds
        self.ax.set_xlim(0, 8); self.ax.set_ylim(0, 8); self.ax.set_zlim(0, 4)
        self.ax.set_axis_off()
        self.ax.view_init(elev=38, azim=-40)
        self.fig.canvas.draw_idle()

    def move_piece(self, fx, fy, tx, ty):
        """Applies spatial logic translation onto the piece system array."""
        if (fx, fy) in self.board:
            asset = self.board[(fx, fy)]
            # Delete old record, update destination index
            del self.board[(fx, fy)]
            self.board[(tx, ty)] = asset
            self.update_visuals()
            print(f">> COMMAND VERIFIED: Moved {asset[0]} from ({fx},{fy}) to ({tx},{ty})")
        else:
            print(">> COMMAND REJECTED: Target source coordinate empty.")

# --- Initialization Control Deck Loop ---
game = CyberChess3D()

# Mount System Input Controls
ax_fx = plt.axes([0.15, 0.18, 0.25, 0.025], facecolor='#161f30')
ax_fy = plt.axes([0.15, 0.13, 0.25, 0.025], facecolor='#161f30')
ax_tx = plt.axes([0.55, 0.18, 0.25, 0.025], facecolor='#161f30')
ax_ty = plt.axes([0.55, 0.13, 0.25, 0.025], facecolor='#161f30')

s_fx = Slider(ax_fx, 'FROM-X', 0, 7, valinit=0, valstep=1, color='#ff0055')
s_fy = Slider(ax_fy, 'FROM-Y', 0, 7, valinit=1, valstep=1, color='#ff0055')
s_tx = Slider(ax_tx, 'TO-X', 0, 7, valinit=0, valstep=1, color='#00ffcc')
s_ty = Slider(ax_ty, 'TO-Y', 0, 7, valinit=3, valstep=1, color='#00ffcc')

for s in [s_fx, s_fy, s_tx, s_ty]:
    s.label.set_color('#ffffff'); s.valtext.set_color('#ffffff')

# Add Tactical Execution Button Trigger
ax_btn = plt.axes([0.4, 0.04, 0.2, 0.04], facecolor='#101b2b')
btn = Button(ax_btn, 'EXECUTE MOVE', color='#060b14', hovercolor='#1e293b')
btn.label.set_color('#00ffcc')
btn.label.set_fontweight('bold')

def trigger_action(event):
    game.move_piece(int(s_fx.val), int(s_fy.val), int(s_tx.val), int(s_ty.val))

btn.on_clicked(trigger_action)

print(">> STRATEGIC BATTLE MATRIX READY.")
plt.show()