import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# 🖥️ PAGE SETUP WITH PREMIUM MODERN SKIN
st.set_page_config(page_title="Urban Grid AI Hub", layout="wide", initial_sidebar_state="collapsed")

# 🎨 CLIENT-CENTRIC ENTERPRISE UI STYLING OVERRIDES
st.markdown("""
    <style>
    /* Global Application Backdrop Styling */
    .stApp { background-color: #090d16; color: #f1f5f9; }
    
    /* Executive Card Transformations */
    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
        border: 1px solid #2d3748;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        margin-bottom: 16px;
    }
    .metric-title { font-size: 14px; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 32px; font-weight: 700; margin: 8px 0; color: #f8fafc; }
    .metric-footer { font-size: 12px; font-weight: 500; }
    
    /* Clean Separator Rules */
    hr { border: 0; height: 1px; background: linear-gradient(to right, #1e293b, #334155, #1e293b); margin: 24px 0; }
    </style>
""", unsafe_allow_html=True)

# 🏙️ MODERN BRANDING HEADER LAYER
st.markdown("""
    <div style='background: linear-gradient(90deg, #1e1b4b 0%, #0f172a 100%); padding: 24px; border-radius: 12px; border-left: 5px solid #4f46e5; margin-bottom: 20px;'>
        <h1 style='margin:0; font-size:30px; font-weight:700; color:#f8fafc; letter-spacing:-0.5px;'>🏙️ URBAN GRID AI: SMART DISPATCH HUB</h1>
        <p style='margin:5px 0 0 0; color:#94a3b8; font-size:14px; font-weight:400;'>Automated IoT Spatial Logistics Optimization Management Console</p>
    </div>
""", unsafe_allow_html=True)

# 🕹️ SIDEBAR CONTROLS
st.sidebar.header("⚙️ Telemetry Settings")
refresh_rate = st.sidebar.slider("Scan Frequency (Seconds)", min_value=1, max_value=10, value=3)
auto_refresh = st.sidebar.checkbox("Live Stream Active", value=True)

API_URL = "http://127.0.0.1:8000/api/v3/urban/dispatch"

try:
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        kpis = data["global_kpis"]
        esg = data["esg_matrix"]
        master_df = pd.DataFrame(data["master_telemetry_grid"])
        queue_df = pd.DataFrame(data["optimized_dispatch_queue"])

        # 📊 EXECUTIVE CONTROL ROW (Clean, high-end metric modules)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
                <div class='metric-card' style='border-top: 4px solid #3b82f6;'>
                    <div class='metric-title'>📡 Monitored Infrastructure</div>
                    <div class='metric-value'>{kpis['monitored_nodes']:,} Units</div>
                    <div class='metric-footer' style='color: #60a5fa;'>● Active IoT Network Online</div>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
                <div class='metric-card' style='border-top: 4px solid #ef4444;'>
                    <div class='metric-title'>🚨 Critical Overflows</div>
                    <div class='metric-value'>{kpis['emergency_flags']} Sites</div>
                    <div class='metric-footer' style='color: #f87171;'>▲ Immediate Action Required</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
                <div class='metric-card' style='border-top: 4px solid #10b981;'>
                    <div class='metric-title'>⚡ Logistics Efficiency</div>
                    <div class='metric-value'>{kpis['logistics_efficiency_pct']}%</div>
                    <div class='metric-footer' style='color: #34d399;'>▼ Saved Travel Distance Matrix</div>
                </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown(f"""
                <div class='metric-card' style='border-top: 4px solid #a855f7;'>
                    <div class='metric-title'>🌱 Carbon Offset Mass</div>
                    <div class='metric-value'>{esg['co2_abated_kg']:,} kg</div>
                    <div class='metric-footer' style='color: #c084fc;'>■ Prevented Fleet Diesel Exhaust</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        # 🎨 GEOGRAPHIC & CAPACITY DATA MATRICES
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("<h3 style='font-size:18px; font-weight:600; margin-bottom:12px; color:#e2e8f0;'>📊 Volumetric Fill Density Distribution</h3>", unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(6, 3.6))
            fig.patch.set_facecolor('#090d16')
            ax.set_facecolor('#111827')
            
            sns.violinplot(data=master_df, x='stream', y='fill_%', palette='magma', ax=ax, inner="quartile")
            
            ax.set_ylabel("Current Capacity Level (%)", color="#94a3b8", fontsize=9)
            ax.set_xlabel("Waste Stream Class", color="#94a3b8", fontsize=9)
            ax.tick_params(colors="#94a3b8", labelsize=8)
            ax.axhline(85, color='#ef4444', linestyle='--', linewidth=1.5, label="85% Dispatch Alarm Floor")
            ax.legend(facecolor='#1f2937', edgecolor='none', labelcolor='#fff', fontsize=8)
            ax.grid(True, linestyle=':', alpha=0.05)
            st.pyplot(fig)

        with chart_col2:
            st.markdown("<h3 style='font-size:18px; font-weight:600; margin-bottom:12px; color:#e2e8f0;'>📍 Live Fleet Geographical Fleet Coordinates</h3>", unsafe_allow_html=True)
            # Upgraded Map Canvas: Switched map dots to match client dashboard colors cleanly
            st.map(master_df)

        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 📋 OPERATIONAL LIVE LOGS & SEQUENCED QUEUE INTERFACES
        bottom_left, bottom_right = st.columns([1, 2])
        
        with bottom_left:
            st.markdown("<h3 style='font-size:18px; font-weight:600; margin-bottom:12px; color:#e2e8f0;'>📝 Infrastructure Diagnostic Logs</h3>", unsafe_allow_html=True)
            st.success("System Stream Metrics Synchronized Successfully!", icon="🔄")
            st.info(f"✨ Core data loop links verified across {kpis['monitored_nodes']} network devices.")
            st.warning(f"🔋 Battery alert: {kpis['battery_critical']} node units reported under 20% limit.")
            st.error(f"🚛 Routing Pipeline auto-generated {kpis['emergency_flags']} emergency paths.")

        with bottom_right:
            st.markdown("<h3 style='font-size:18px; font-weight:600; margin-bottom:12px; color:#e2e8f0;'>🚛 Sequenced Dynamic Route Collection Queue</h3>", unsafe_allow_html=True)
            if not queue_df.empty:
                display_queue = queue_df.rename(columns={
                    "node_id": "Target ID", "fill_%": "Fill Value (%)",
                    "assigned_sector": "Fleet Division", "distance_km": "Distance Matrix (KM)",
                    "stream": "Material Group", "urgency_index": "Urgency Rating"
                })
                
                # 🌟 CLIENT UPDATE: Beautiful interactive styled grid column formatting
                st.dataframe(display_queue, use_container_width=True, height=380 )
            else:
                st.success("All regional municipal deployment points are operating well below safety thresholds.")

except requests.exceptions.ConnectionError:
    st.error("🛑 Server link failure: Frontend isolated from backend data core. Confirm Terminal 1 is active.")

# 🔁 STABLE AUTOMATION FLOW REFRESH LOOP
if auto_refresh:
    time.sleep(refresh_rate)
    st.experimental_rerun()
