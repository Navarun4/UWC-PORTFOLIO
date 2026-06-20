import tkinter as tk
from tkinter import ttk
import random

# ==========================================
# 1. CORE DATA MODEL WITH INJECTION MECHANICS
# ==========================================
class WasteNode:
    def __init__(self, node_id, zone_name, baseline_generation, x, y):
        self.node_id = node_id
        self.zone_name = zone_name
        self.capacity_kg = 500
        self.current_waste_kg = random.uniform(60, 140)
        self.hourly_growth_rate = baseline_generation
        self.x = x
        self.y = y

    def update_waste(self, speed_modifier):
        """Simulates growth cycles scaling dynamically with UI slider inputs"""
        growth = ((self.hourly_growth_rate * 0.04) + random.uniform(-0.1, 0.6)) * speed_modifier
        self.current_waste_kg = min(self.capacity_kg, self.current_waste_kg + max(0, growth))

    def inject_waste(self, amount=100):
        """Allows user to manually spike waste levels via UI"""
        self.current_waste_kg = min(self.capacity_kg, self.current_waste_kg + amount)

    def get_fill_percentage(self):
        return (self.current_waste_kg / self.capacity_kg) * 100

    def get_hex_color(self):
        pct = self.get_fill_percentage()
        if pct < 50: return "#10B981"  # Emerald Green
        if pct < 75: return "#F59E0B"  # Amber Orange
        return "#EF4444"              # Vivid Red


# ==========================================
# 2. PREMIUM CYBER LOGISTICS COMMAND CENTER
# ==========================================
class CyberLogisticsEngine:
    def __init__(self, root, nodes):
        self.root = root
        self.root.title("NEO-GRID: Intelligent Logistics Command Suite")
        self.root.geometry("1180x720")
        self.root.configure(bg="#111827") # Deep Slate Dark Mode
        
        self.nodes = nodes
        self.total_carbon_saved = 0.0
        
        # Vehicle Navigation Properties
        self.depot_x, self.depot_y = 80, 500
        self.truck_x = self.depot_x
        self.truck_y = self.depot_y
        self.truck_target = None
        self.system_paused = False

        self.setup_premium_ui()
        self.engine_heartbeat_loop()

    def setup_premium_ui(self):
        """Builds a beautiful modern software dashboard"""
        # Style adjustments for ttk widgets
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Horizontal.TScale", background="#1F2937", troughcolor="#374151")

        # --- HEADER BANNER ---
        header = tk.Frame(self.root, bg="#1F2937", height=70, bd=0, highlightthickness=0)
        header.pack(fill="x")
        
        title_frame = tk.Frame(header, bg="#1F2937")
        title_frame.pack(side="left", padx=25, pady=15)
        
        title = tk.Label(title_frame, text="NEO-GRID INDUSTRIAL", fg="#F9FAFB", bg="#1F2937", font=("Code Pro", 14, "bold"))
        title.pack(anchor="w")
        subtitle = tk.Label(title_frame, text="Automated Eco-Logistics Optimization Engine", fg="#9CA3AF", bg="#1F2937", font=("Helvetica", 9))
        subtitle.pack(anchor="w")

        # Visual Status Engine LED Light Indicator
        self.led_frame = tk.Frame(header, bg="#1F2937")
        self.led_frame.pack(side="right", padx=25)
        self.lbl_led_light = tk.Label(self.led_frame, text="● ENGINE ACTIVE", fg="#10B981", bg="#1F2937", font=("Helvetica", 10, "bold"))
        self.lbl_led_light.pack(side="right", padx=5)

        # --- MAIN WORKSPACE SPLITTER ---
        workspace = tk.Frame(self.root, bg="#111827")
        workspace.pack(fill="both", expand=True, padx=20, pady=20)

        # --- LEFT CONTROLS SIDEBAR ---
        sidebar = tk.Frame(workspace, bg="#1F2937", width=420, padx=18, pady=15)
        sidebar.pack(side="left", fill="y", padx=(0, 15))
        
        tk.Label(sidebar, text="URBAN SECTOR OVERVIEWS", fg="#F3F4F6", bg="#1F2937", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(0, 10))
        
        self.ui_labels = {}
        
        # Sector Control Row Modules
        for node in self.nodes:
            row_card = tk.Frame(sidebar, bg="#111827", pady=8, padx=10)
            row_card.pack(fill="x", pady=5)
            
            lbl_name = tk.Label(row_card, text=node.zone_name.split(" (")[0], fg="#F9FAFB", bg="#111827", font=("Helvetica", 9, "bold"))
            lbl_name.pack(side="left", anchor="w")
            
            # Action Button 1: Inject Trash
            btn_inject = tk.Button(row_card, text="Inject ➕", font=("Helvetica", 8, "bold"), bg="#374151", fg="#F3F4F6",
                                   activebackground="#4B5563", activeforeground="white", relief="flat", bd=0, padx=6,
                                   command=lambda n=node: self.manual_inject_waste(n))
            btn_inject.pack(side="right", padx=(5, 0))

            # Action Button 2: Manual Clean Empty Flush
            btn_flush = tk.Button(row_card, text="Empty 🗑️", font=("Helvetica", 8, "bold"), bg="#D97706", fg="white",
                                  activebackground="#B45309", activeforeground="white", relief="flat", bd=0, padx=6,
                                  command=lambda n=node: self.manual_flush_node(n))
            btn_flush.pack(side="right", padx=(5, 0))
            
            lbl_pct = tk.Label(row_card, text="0.0%", fg="#10B981", bg="#111827", font=("Helvetica", 10, "bold"))
            lbl_pct.pack(side="right", anchor="e", padx=5)
            
            self.ui_labels[node.node_id] = lbl_pct

        # --- INTERACTIVE HARDWARE METERS ---
        tk.Label(sidebar, text="GRID SIMULATION RATE", fg="#F3F4F6", bg="#1F2937", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(20, 5))
        
        slider_box = tk.Frame(sidebar, bg="#111827", padx=12, pady=10)
        slider_box.pack(fill="x", pady=5)
        
        tk.Label(slider_box, text="Global Accretion Velocity Multiplier", fg="#9CA3AF", bg="#111827", font=("Helvetica", 8, "bold")).pack(anchor="w")
        self.speed_slider = ttk.Scale(slider_box, from_=0.0, to=5.0, orient="horizontal", style="Horizontal.TScale")
        self.speed_slider.set(1.0)
        self.speed_slider.pack(fill="x", pady=(8, 0))

        # Core Action Play Pause Button
        self.btn_pause = tk.Button(sidebar, text="Pause System Execution ⏸️", font=("Helvetica", 10, "bold"), bg="#2563EB", fg="white", relief="flat", bd=0, pady=8, command=self.toggle_system_state)
        self.btn_pause.pack(fill="x", pady=(15, 0))

        # --- REAL-TIME DATA LOG ENGINE ---
        tk.Label(sidebar, text="ANALYTICS TELEMETRY", fg="#F3F4F6", bg="#1F2937", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(25, 5))
        
        self.lbl_status = tk.Label(sidebar, text="Awaiting tracking matrices...", fg="#9CA3AF", bg="#1F2937", font=("Helvetica", 9), wraplength=360, justify="left")
        self.lbl_status.pack(anchor="w", pady=4)
        
        self.lbl_carbon = tk.Label(sidebar, text="Carbon Mitigated: 0.00 kg CO2e", fg="#10B981", bg="#1F2937", font=("Helvetica", 12, "bold"))
        self.lbl_carbon.pack(anchor="w", pady=10)

        # --- RIGHT CANVAS MAP GRID VIEWPORT ---
        self.canvas = tk.Canvas(workspace, bg="#111827", highlightthickness=1, highlightbackground="#374151")
        self.canvas.pack(side="right", fill="both", expand=True)

    def toggle_system_state(self):
        """Toggles the runtime simulation architecture"""
        self.system_paused = not self.system_paused
        if self.system_paused:
            self.btn_pause.config(text="Resume System Execution ▶️", bg="#059669")
            self.lbl_led_light.config(text="● ENGINE PAUSED", fg="#EF4444")
            self.lbl_status.config(text="System Architecture Paused. Clock processes halted.")
        else:
            self.btn_pause.config(text="Pause System Execution ⏸️", bg="#2563EB")
            self.lbl_led_light.config(text="● ENGINE ACTIVE", fg="#10B981")
            self.lbl_status.config(text="System Architecture Resumed. Continuing monitoring sweeps...")

    def manual_inject_waste(self, node):
        """Allows user to force feed 100kg of trash instantly into any target node sector card"""
        node.inject_waste(100)
        self.lbl_status.config(text=f"⚡ Injection Trigger: Pumped +100kg of stress load directly into {node.zone_name}!")

    def manual_flush_node(self, node):
        """Clears a bin completely, instantly invoking dynamic re-routing if the truck is heading here"""
        node.current_waste_kg = 0.0
        self.lbl_status.config(text=f"🔧 User Override: Dumped storage values back to 0% at {node.zone_name}!")
        
        # CRITICAL DYNAMIC RE-ROUTING FIX: If truck was moving here, drop target so it updates immediately!
        if self.truck_target and getattr(self.truck_target, 'node_id', None) == node.node_id:
            print(f"[RE-ROUTING EVENT] Target sector {node.zone_name} manually flushed. Recalculating path routes.")
            self.truck_target = None 

    def engine_heartbeat_loop(self):
        """Main logical frame processing evaluation system loops"""
        if not self.system_paused:
            speed_modifier = self.speed_slider.get()

            # Process natural accumulation only when truck isn't forcing navigation steps or handles re-routing checks
            if self.truck_target is None:
                for node in self.nodes:
                    node.update_waste(speed_modifier)
                
                # Check for sectors needing evacuation emergency dispatches
                critical_nodes = [n for n in self.nodes if n.get_fill_percentage() >= 75]
                if critical_nodes:
                    self.truck_target = critical_nodes[0]
            
            # Vehicle Navigation Vectors Path Calculations Frame Blocks
            if self.truck_target is not None:
                tx, ty = self.truck_target.x, self.truck_target.y
                
                dx = tx - self.truck_x
                dy = ty - self.truck_y
                distance_to_vector = (dx**2 + dy**2)**0.5
                
                navigation_speed = 7.0
                if distance_to_vector > navigation_speed:
                    self.truck_x += (dx / distance_to_vector) * navigation_speed
                    self.truck_y += (dy / distance_to_vector) * navigation_speed
                    
                    if tx == self.depot_x and ty == self.depot_y:
                        self.lbl_status.config(text="🚚 Target cleared or processed. Truck returning to Depot Base station.")
                    else:
                        self.lbl_status.config(text=f"🛰️ Dispatch actively locked and moving towards: {self.truck_target.zone_name}.")
                else:
                    self.truck_x, self.truck_y = tx, ty
                    
                    if tx == self.depot_x and ty == self.depot_y:
                        self.truck_target = None
                        self.lbl_status.config(text="🟢 Truck safely docked at Depot Base. Sweeping grid channels.")
                    else:
                        # Arrived cleanly over target node sector cluster location
                        self.lbl_status.config(text=f"🧹 Purging storage bins... Processing environmental savings analytics at {self.truck_target.zone_name}...")
                        
                        opt_dist = random.uniform(3.5, 7.2)
                        saved_dist = (opt_dist * 1.45) - opt_dist
                        self.total_carbon_saved += (saved_dist * 0.411)
                        
                        self.truck_target.current_waste_kg = 0.0 # Clean output fields back down to absolute base values
                        
                        # Command routing back home to Central Base station array location hooks
                        class DepotTargetCoordinates:
                            x = self.depot_x
                            y = self.depot_y
                            zone_name = "Central Depot"
                        self.truck_target = DepotTargetCoordinates()

        # --- LAYOUT REDRAW PASS PAINT CYCLE MAP CANVAS ELEMENTS ---
        self.canvas.delete("all")
        
        # Render clean dark mode interconnect wire conduits lines
        for node in self.nodes:
            self.canvas.create_line(self.depot_x, self.depot_y, node.x, node.y, fill="#374151", width=2, dash=(6, 4))
            
        # Draw central structural depot headquarters docking base platform
        self.canvas.create_rectangle(self.depot_x-25, self.depot_y-25, self.depot_x+25, self.depot_y+25, fill="#1F2937", outline="#2563EB", width=2)
        self.canvas.create_text(self.depot_x, self.depot_y, text="DEPOT", fill="#F9FAFB", font=("Helvetica", 8, "bold"))
        
        # Render and update geographic node sector positions 
        for node in self.nodes:
            hex_color = node.get_hex_color()
            fill_pct = node.get_fill_percentage()
            
            # Sync labels sideboards values displays metrics fields variables
            self.ui_labels[node.node_id].config(text=f"{fill_pct:.1f}% ({int(node.current_waste_kg)}kg)", fg=hex_color)
            
            # Node scale maps layout circle expansion properties tracking logic indices variables
            radius = 22 + int(fill_pct * 0.18)
            self.canvas.create_oval(node.x-radius, node.y-radius, node.x+radius, node.y+radius, fill=hex_color, outline="#111827", width=3)
            self.canvas.create_text(node.x, node.y-6, text=f"S{node.node_id}", fill="#111827", font=("Helvetica", 10, "bold"))
            self.canvas.create_text(node.x, node.y+10, text=f"{int(fill_pct)}%", fill="#111827", font=("Helvetica", 8, "bold"))

        # Render Active Logistics Transporter Entity Fleet Layer Tracking Components
        self.canvas.create_oval(self.truck_x-14, self.truck_y-14, self.truck_x+14, self.truck_y+14, fill="#F59E0B", outline="#F9FAFB", width=2)
        self.canvas.create_text(self.truck_x, self.truck_y, text="🚚", font=("Helvetica", 11))

        # Synchronize analytics data labels fields counters
        self.lbl_carbon.config(text=f"Carbon Mitigated: {self.total_carbon_saved:.2f} kg CO2e")

        # Schedule next refresh cycle frame processing updates cadence loops (~30FPS speed operations defaults)
        self.root.after(33, self.engine_heartbeat_loop)


# ==========================================
# 3. RUNTIME APP SYSTEM INTIALIZATION CORE
# ==========================================
if __name__ == "__main__":
    # Spatial configuration properties maps setup grid targets metrics
    sectors = [
        WasteNode(1, "Sector Alpha (Commercial)", 35.0, x=200, y=130),
        WasteNode(2, "Sector Beta (Residential)", 18.0, x=500, y=100),
        WasteNode(3, "Sector Gamma (Industrial)", 60.0, x=550, y=350),
        WasteNode(4, "Sector Delta (Institutional)", 26.0, x=240, y=320)
    ]
    
    app_root = tk.Tk()
    system_suite = CyberLogisticsEngine(app_root, sectors)
    app_root.mainloop()