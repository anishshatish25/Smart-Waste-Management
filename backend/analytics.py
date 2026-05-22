import numpy as np
import pandas as pd
import time
def generate_metropolitan_grid(num_nodes=1000):
    np.random.seed(int(time.time()))
    node_ids = [f"NODE-{str(i).zfill(3)}" for i in range(1, num_nodes + 1)]
    latitudes = np.random.normal(loc=40.7128, scale=0.035, size=num_nodes)
    longitudes = np.random.normal(loc=-74.0060, scale=0.035, size=num_nodes)
    fill_levels = np.random.randint(5, 101, size=num_nodes)
    battery_levels = np.random.randint(10, 101, size=num_nodes)
    waste_streams = np.random.choice(['Bio-Hazard', 'Recyclables', 'Glass-Composites', 'General Solid'], size=num_nodes)
    days_stagnant = np.random.randint(1, 10, size=num_nodes)
    
    return pd.DataFrame({
        'node_id': node_ids, 'latitude': latitudes, 'longitude': longitudes,
        'fill_%': fill_levels, 'battery_%': battery_levels, 'stream': waste_streams,
        'stagnant_days': days_stagnant
    })

def compute_command_center_metrics():
    df = generate_metropolitan_grid()
    df['urgency_index'] = (df['fill_%'] * 0.6) + (df['stagnant_days'] * 4.0) - (df['battery_%'] * 0.1)
    df['urgency_index'] = df['urgency_index'].clip(lower=0).round(1)
    
    df['status'] = np.where(df['fill_%'] > 85, 'CRITICAL DISPATCH',
                            np.where(df['fill_%'] > 55, 'SCHEDULED WARNING', 'STABLE NOMINAL'))
    
    critical_mask = df['status'] == 'CRITICAL DISPATCH'
    critical_df = df[critical_mask].copy()
    depot_coords = np.array([40.7128, -74.0060])
    
    if not critical_df.empty:
        critical_coords = critical_df[['latitude', 'longitude']].values
        distances_from_depot = np.linalg.norm(critical_coords - depot_coords, axis=1) * 111.12
        critical_df['distance_km'] = distances_from_depot.round(2)
        
        angles = np.arctan2(critical_coords[:, 0] - depot_coords[0], critical_coords[:, 1] - depot_coords[1])
        critical_df['assigned_sector'] = np.where(angles > 1.5, 'Bronx Logistics Hub',
                                                   np.where(angles > 0, 'Queens Sector',
                                                            np.where(angles > -1.5, 'Brooklyn Heights', 'Manhattan Core')))
        
        optimized_df = critical_df.sort_values(by=['assigned_sector', 'distance_km'])
        routing_queue = optimized_df[['node_id', 'fill_%', 'assigned_sector', 'distance_km', 'stream', 'urgency_index']].to_dict(orient='records')
        
        fleet_optimized_distance = float(distances_from_depot.sum() * 1.25)
        legacy_unoptimized_distance = float(len(critical_df) * 14.5)
        kilometers_saved = max(0.0, legacy_unoptimized_distance - fleet_optimized_distance)
        diesel_saved_liters = kilometers_saved * 0.38
        carbon_prevented_kg = diesel_saved_liters * 2.68
        efficiency_score = round((kilometers_saved / legacy_unoptimized_distance) * 100, 1)
    else:
        routing_queue, diesel_saved_liters, carbon_prevented_kg, efficiency_score = [], 0.0, 0.0, 100.0

    stream_averages = df.groupby('stream')['fill_%'].mean().round(1).to_dict()

    # 🌟 CRITICAL FIX: Ensure keys match what the frontend expects exactly
    return {
        "global_kpis": {
            "monitored_nodes": len(df),
            "emergency_flags": int(critical_mask.sum()),
            "battery_critical": int((df['battery_%'] < 20).sum()),
            "logistics_efficiency_pct": efficiency_score
        },
        "esg_matrix": {
            "fuel_saved_l": round(diesel_saved_liters, 1),
            "co2_abated_kg": round(carbon_prevented_kg, 1)
        },
        "stream_analytics": stream_averages,
        "optimized_dispatch_queue": routing_queue,
        "master_telemetry_grid": df.to_dict(orient='records')
    }
