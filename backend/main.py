import numpy as np
import pandas as pd
import matplotlib
# Use a non-interactive backend for Matplotlib so it runs silently without looking for a GUI window
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Urban Grid AI Logistics Engine", version="4.0.0")

# 🔌 ALLOW FRONTEND TO CONNECT (Fixes CORS Security Blocks)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a static directory to host our Seaborn generated visualization figures safely
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

def generate_metropolitan_grid(num_nodes=1000):
    """
    Generates real-time IoT dataset tracking nodes mapped across 
    actual real-world city location clusters using angular sector quadrants.
    """
    depot_coords = [40.730610, -73.935242]
    node_ids = [f"NODE-{str(i).zfill(3)}" for i in range(1, num_nodes + 1)]
    streams = ['Recyclables', 'General Solid', 'Bio-Hazard', 'Glass-Composites']
    
    data = []
    for node_id in node_ids:
        stream = np.random.choice(streams)
        lat = depot_coords[0] + np.random.uniform(-0.08, 0.08)
        lon = depot_coords[1] + np.random.uniform(-0.12, 0.12)
        fill_pct = int(np.random.uniform(10, 100))
        # 🔋 NumPy: Simulate IoT Node internal battery level percentages
        battery_pct = int(np.random.uniform(5, 100))
        
        data.append({
            "node_id": node_id,
            "stream": stream,
            "latitude": lat,
            "longitude": lon,
            "fill_%": fill_pct,
            "battery_%": battery_pct
        })
        
    df = pd.DataFrame(data)
    critical_mask = df["fill_%"] >= 85
    critical_df = df[critical_mask].copy()
    
    if not critical_df.empty:
        critical_coords = critical_df[['latitude', 'longitude']].values
        distances_from_depot = np.linalg.norm(critical_coords - depot_coords, axis=1) * 111.12
        critical_df['distance_km'] = distances_from_depot.round(2)
        
        # 🏙️ GEOGRAPHIC QUADRANT DIRECTIONAL MATH
        angles = np.arctan2(critical_coords[:, 0] - depot_coords[0], critical_coords[:, 1] - depot_coords[1])
        critical_df['assigned_sector'] = np.where(angles > 1.5, 'Bronx Logistics Hub',
                                         np.where(angles > 0, 'Queens Sector',
                                         np.where(angles > -1.5, 'Brooklyn Heights', 'Manhattan Core')))
        
        # Urgency score matrix logic
        critical_df['urgency_index'] = (critical_df['fill_%'] * 0.7) + ((25 - critical_df['distance_km']) * 0.3)
        routing_queue = critical_df.sort_values(by="urgency_index", ascending=False)
        
        emergency_flags = int(critical_mask.sum())
        efficiency_score = round((emergency_flags * 0.45) + 40, 1)
    else:
        routing_queue = pd.DataFrame()
        efficiency_score = 100.0
        emergency_flags = 0

    return df, routing_queue, efficiency_score, emergency_flags

def render_seaborn_analytics(df):
    """
    🎨 Matplotlib & Seaborn Engine: Generates a premium correlation plot 
    tracking the data relationships between bin capacities and node battery life.
    """
    plt.figure(figsize=(6, 4))
    # Dark modern theme matching your frontend layout
    plt.style.use('dark_background')
    
    # Seaborn kernel density estimate distribution plot
    sns.kdeplot(data=df, x="fill_%", y="battery_%", cmap="mako", fill=True, thresh=0.05, cbar=True)
    
    plt.title("IoT Telemetry Joint Density Plot Matrix", fontsize=10, pad=10, color="#cbd5e1")
    plt.xlabel("Fill Capacity (%)", fontsize=8, color="#94a3b8")
    plt.ylabel("Battery Level (%)", fontsize=8, color="#94a3b8")
    plt.tick_params(colors='#64748b', labelsize=7)
    plt.tight_layout()
    
    # Save chart cleanly to static server assets
    plot_path = os.path.join("static", "seaborn_chart.png")
    plt.savefig(plot_path, dpi=150, facecolor='#121720')
    plt.close()

@app.get("/api/v3/urban/dispatch")
def get_dispatch_metrics():
    df, routing_queue, efficiency_score, emergency_flags = generate_metropolitan_grid()
    
    # Run the Matplotlib and Seaborn analytics renderer pipeline smoothly
    render_seaborn_analytics(df)
    
    dispatch_list = []
    if not routing_queue.empty:
        dispatch_list = routing_queue.head(10).to_dict(orient="records")

    def get_target_bin(stream_type):
        if not routing_queue.empty:
            match = routing_queue[routing_queue['stream'] == stream_type]
            if not match.empty:
                top_bin = match.iloc[0]
                return f"{top_bin['node_id']} ({top_bin['assigned_sector']})"
        return "Scanning Grid..."

    statuses = ["En Route", "Arrived", "Collecting", "Clearing", "Returning"]
    
    # 🔎 Pandas & NumPy Diagnostic Log Engine Counters
    low_battery_count = int((df["battery_%"] < 20).sum())
    bio_hazard_overflows = int(((df["stream"] == "Bio-Hazard") & (df["fill_%"] >= 85)).sum())
    pipeline_bypasses = int((df["fill_%"] >= 95).sum())

    payload = {
        "global_kpis": {
            "monitored_nodes": len(df),
            "emergency_flags": emergency_flags,
            "logistics_efficiency_pct": min(efficiency_score, 94.2)
        },
        "esg_matrix": {
            "co2_abated_kg": round(emergency_flags * 8.4, 1)
        },
        "master_telemetry_grid": df[["latitude", "longitude", "fill_%"]].to_dict(orient="records"),
        "optimized_dispatch_queue": dispatch_list,
        
        "fleet_status": [
            {"id": "TRUCK-A1", "type": "Bio-Hazard Specialist", "status": np.random.choice(statuses), "assigned_target": get_target_bin('Bio-Hazard'), "color": "red"},
            {"id": "TRUCK-B2", "type": "Recycling Logistician", "status": np.random.choice(statuses), "assigned_target": get_target_bin('Recyclables'), "color": "emerald"},
            {"id": "TRUCK-C3", "type": "General Solid Hauler", "status": np.random.choice(statuses), "assigned_target": get_target_bin('General Solid'), "color": "amber"},
            {"id": "TRUCK-D4", "type": "Heavy Glass Compactor", "status": np.random.choice(statuses), "assigned_target": get_target_bin('Glass-Composites'), "color": "blue"}
        ],
        
        # 📝 INFRASTRUCTURE DIAGNOSTIC DATA PAYLOAD
        "diagnostic_logs": {
            "device_link_status": "Verified",
            "low_battery_units": low_battery_count,
            "bio_hazard_alerts": bio_hazard_overflows,
            "critical_bypasses": pipeline_bypasses
        },
        
        # 🖼️ SEABORN FILEPATH LINKER
        "seaborn_plot_url": "http://127.0.0.1:8000/static/seaborn_chart.png?v=" + str(np.random.randint(0, 100000))
    }
    return payload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
