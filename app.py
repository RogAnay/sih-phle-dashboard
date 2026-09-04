# =============================================================================
#  app.py — PHLE: Predictive Healthcare Logistics Ecosystem
#  Smart India Hackathon | Ministry of Health & Family Welfare
# =============================================================================
import math
import os
import random
import warnings
from typing import Dict, List

import folium
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

warnings.filterwarnings("ignore")

# =============================================================================
# §1  PAGE CONFIGURATION & CSS
# =============================================================================
st.set_page_config(page_title="PHLE | SIH", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

_CSS = """
<style>
/* Import High-Tech Typography */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg-dark: #050811;
    --card-bg: #0b1320;
    --border-color: #1a2a40;
    --border-highlight: #254066;
    --accent-blue: #2a8cff;
    --text-primary: #e6f1ff;
    --text-secondary: #6482a6;
}

/* Base Body Styling */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp { 
    background: var(--bg-dark); 
    color: var(--text-primary); 
}

/* Sidebar Dark Theme & Clean Borders */
section[data-testid="stSidebar"] { 
    background: linear-gradient(180deg, #070e1b 0%, #030710 100%); 
    border-right: 1px solid var(--border-color); 
}

.stApp [data-testid="stHeader"] { 
    background: transparent; 
}

/* Section Header Bar Styling (.sec) */
.sec { 
    border-left: 4px solid var(--accent-blue); 
    background: linear-gradient(90deg, rgba(42, 140, 255, 0.12) 0%, rgba(11, 19, 32, 0.0) 100%); 
    border-radius: 0 8px 8px 0; 
    color: #f0f6ff; 
    font-size: 0.95rem; 
    font-weight: 800; 
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 8px 16px; 
    margin: 24px 0 16px 0; 
    display: flex;
    align-items: center;
    box-shadow: inset 1px 0 0 rgba(255, 255, 255, 0.05);
}

/* KPI Card Grid Polish & Hover Animations (.kpi) */
.kpi { 
    background: var(--card-bg); 
    border: 1px solid var(--border-color); 
    border-top: 3px solid var(--accent-blue); 
    border-radius: 12px; 
    padding: 18px 20px; 
    height: 115px; 
    display: flex; 
    flex-direction: column; 
    justify-content: space-between; 
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.kpi::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at top right, rgba(42, 140, 255, 0.08), transparent 70%);
    pointer-events: none;
}

.kpi:hover {
    transform: translateY(-4px);
    border-color: var(--accent-blue);
    box-shadow: 0 8px 24px -4px rgba(42, 140, 255, 0.25),
                0 0 12px 0 rgba(42, 140, 255, 0.15);
}

.kpi-label { 
    color: var(--text-secondary); 
    font-size: 0.72rem; 
    font-weight: 700; 
    letter-spacing: 1.2px; 
    text-transform: uppercase; 
}

.kpi-value { 
    color: #ffffff; 
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.1rem; 
    font-weight: 800; 
    line-height: 1; 
    letter-spacing: -0.5px;
}

.kpi-delta-pos  { color: #34d484; font-size: 0.78rem; font-weight: 700; display: flex; align-items: center; gap: 4px; }
.kpi-delta-neg  { color: #f45c5c; font-size: 0.78rem; font-weight: 700; display: flex; align-items: center; gap: 4px; }
.kpi-delta-warn { color: #f0a030; font-size: 0.78rem; font-weight: 700; display: flex; align-items: center; gap: 4px; }

/* Telemetry Cards (.tele) */
.tele { 
    background: var(--card-bg); 
    border: 1px solid var(--border-color); 
    border-bottom: 3px solid var(--accent-blue); 
    border-radius: 12px; 
    padding: 16px; 
    text-align: center; 
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.tele:hover {
    transform: translateY(-2px);
    border-color: var(--accent-blue);
}

.tele-val { 
    color: var(--accent-blue); 
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem; 
    font-weight: 800; 
    margin: 4px 0 2px; 
}

.tele-lbl { 
    color: var(--text-secondary); 
    font-size: 0.70rem; 
    font-weight: 700;
    text-transform: uppercase; 
    letter-spacing: 1.2px; 
}

/* Ribbons & Alerts */
.ribbon-crit { 
    border-left: 4px solid #e53535; 
    background: rgba(229, 53, 53, 0.12); 
    padding: 10px 16px; 
    border-radius: 0 8px 8px 0; 
    color: #ff9999; 
    font-size: 0.85rem; 
    font-weight: 600;
    margin: 12px 0; 
}

/* Table & Chart Alignment Fixes */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
    background-color: var(--card-bg);
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}

/* Map iFrame Alignment */
iframe {
    border-radius: 12px !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}

/* Native Chart Containers Overrides */
div[data-testid="stVegaLiteChart"] {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}

/* Scrollbar Tweaks */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg-dark);
}
::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--border-highlight);
}
</style>
"""
st.markdown(_CSS, unsafe_allow_html=True)# =============================================================================
# §2  CONSTANTS & DATA ENGINE
# =============================================================================
COMMODITIES = ["Paracetamol 500mg", "ORS Sachets", "IV Fluids — NS 500 ml", "Oxygen Cylinders"]
VEHICLE_POOL = {"cold": ["Reefer Van (2T)", "Insulated Ambulance"], "standard": ["Mini Truck (2T)", "State Health Van", "Tempo Traveller"]}
FACILITY_PROFILES = {"District": {"burn_rate": 8.0, "occupancy": 0.88}, "Sub-District": {"burn_rate": 6.0, "occupancy": 0.82}, "CHC": {"burn_rate": 4.5, "occupancy": 0.78}, "PHC": {"burn_rate": 3.0, "occupancy": 0.70}, "Default": {"burn_rate": 3.5, "occupancy": 0.75}}
URGENCY_HEX = {"Critical": "#e53535", "Imminent": "#f0a030", "Surplus": "#28c76f"}

def infer_facility_type(name: str) -> str:
    n = str(name).upper()
    if any(k in n for k in ("DISTRICT", "SDH", "HOSPITAL")): return "Sub-District"
    if any(k in n for k in ("CHC", "CARE", "CLINIC")): return "CHC"
    if any(k in n for k in ("PHC", "POST", "CENTRE", "CENTER")): return "PHC"
    return "Default"

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2, dphi, dlam = map(math.radians, [lat1, lat2, lat2 - lat1, lon2 - lon1])
    a = math.sin(dphi / 2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam / 2)**2
    return round(R * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a)), 1)

@st.cache_data(show_spinner=False)
def load_data(path="hospitals.csv"):
    if not os.path.exists(path):
        st.error(f"{path} not found.")
        st.stop()
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    return df

def enrich_data(raw: pd.DataFrame, surge: float, buffer: int) -> pd.DataFrame:
    df = raw.copy()
    df["Current Medicine Stock"] = pd.to_numeric(df["Current Medicine Stock"], errors="coerce").fillna(0)
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    
    df["Facility Type"] = df["Hospital Name"].apply(infer_facility_type)
    df["Burn Rate"] = df["Facility Type"].map(lambda t: FACILITY_PROFILES.get(t, {}).get("burn_rate", 3.5))
    df["Effective Burn"] = (df["Burn Rate"] * surge).round(2)
    df["Days Left"] = (df["Current Medicine Stock"] / df["Effective Burn"]).round(1)
    
    def get_urgency(days):
        if days < (buffer * 0.6): return "Critical"
        if days < buffer: return "Imminent"
        return "Surplus"
        
    df["Urgency"] = df["Days Left"].apply(get_urgency)
    df["Severity Index"] = df["Days Left"].apply(lambda d: round(max(0.0, min(10.0, (buffer - d) * 1.5)), 1))
    df["Projected Stock"] = df["Current Medicine Stock"].copy()
    return df

def calculate_reroute(df: pd.DataFrame, cold: bool) -> List[Dict]:
    surplus = df[df["Urgency"] == "Surplus"].copy()
    deficit = df[df["Urgency"].isin(["Critical", "Imminent"])].sort_values("Days Left", ascending=True)
    if surplus.empty or deficit.empty: return []
        
    routes, rng = [], random.Random(42)
    pool = VEHICLE_POOL["cold"] if cold else VEHICLE_POOL["standard"]
    surplus_balances = surplus.set_index("Hospital Name")["Current Medicine Stock"].to_dict()
    
    for _, drow in deficit.iterrows():
        d_name, d_lat, d_lon = drow["Hospital Name"], float(drow["Latitude"]), float(drow["Longitude"])
        needed = int((drow["Effective Burn"] * 5) - drow["Current Medicine Stock"])
        if needed <= 0: needed = 10
        
        best_hub, min_dist = None, float("inf")
        for s_name, bal in surplus_balances.items():
            if bal > 15:
                srow = surplus[surplus["Hospital Name"] == s_name].iloc[0]
                dist = haversine_km(d_lat, d_lon, float(srow["Latitude"]), float(srow["Longitude"]))
                if dist < min_dist:
                    min_dist, best_hub = dist, s_name
                    
        if best_hub:
            alloc = min(needed, int(surplus_balances[best_hub] * 0.5))
            if alloc > 0:
                surplus_balances[best_hub] -= alloc
                s_match = surplus[surplus["Hospital Name"] == best_hub].iloc[0]
                road_dist = round(min_dist * 1.25, 1)
                routes.append({
                    "Origin": best_hub, "Destination": d_name,
                    "from_lat": float(s_match["Latitude"]), "from_lon": float(s_match["Longitude"]),
                    "to_lat": d_lat, "to_lon": d_lon,
                    "Allocated Units": alloc, "Road Distance (km)": road_dist,
                    "Transit Time (hrs)": round(road_dist / 45.0, 1),
                    "Vehicle Type": rng.choice(pool),
                    "Cost (INR)": round(road_dist * 32.0, 0),
                    "CO2 (kg)": round(road_dist * 0.21, 2)
                })
    return routes

# =============================================================================
# §3  SIDEBAR & RUNTIME STATE
# =============================================================================
st.sidebar.markdown('### 🏥 PHLE Control Console')
commodity = st.sidebar.selectbox("Critical Commodity:", COMMODITIES)
surge = st.sidebar.slider("Outbreak Surge Multiplier:", 1.0, 3.0, 1.2, 0.1)
buffer = st.sidebar.slider("Reserve Buffer Days:", 1, 15, 3, 1)
cold = st.sidebar.toggle("Cold-Chain Transit Protocol", value=False)

if "active" not in st.session_state: st.session_state["active"] = False

c_b1, c_b2 = st.sidebar.columns(2)
if c_b1.button("⚡ Reroute", use_container_width=True, type="primary"): st.session_state["active"] = True
if c_b2.button("Reset", use_container_width=True): st.session_state["active"] = False

# =============================================================================
# §4  DATA PROCESSING & TOP KPIS
# =============================================================================
df = enrich_data(load_data("hospitals.csv"), surge, buffer)

routes: List[Dict] = []
if st.session_state["active"]:
    routes = calculate_reroute(df, cold)
    for r in routes:
        df.loc[df["Hospital Name"] == r["Destination"], "Projected Stock"] += r["Allocated Units"]
        df.loc[df["Hospital Name"] == r["Origin"], "Projected Stock"] -= r["Allocated Units"]

crit_count, immn_count, surp_count = sum(df["Urgency"]=="Critical"), sum(df["Urgency"]=="Imminent"), sum(df["Urgency"]=="Surplus")

st.markdown('<div class="sec">Executive Overview</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f'<div class="kpi"><span class="kpi-label">Monitored Facilities</span><span class="kpi-value">{len(df)}</span><span class="kpi-delta-pos">100% Active</span></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="kpi"><span class="kpi-label">Critical Shortages</span><span class="kpi-value">{crit_count}</span><span class="kpi-delta-neg">Emergency Action</span></div>', unsafe_allow_html=True)
k3.markdown(f'<div class="kpi"><span class="kpi-label">Imminent Risk</span><span class="kpi-value">{immn_count}</span><span class="kpi-delta-warn">Buffer Deficit</span></div>', unsafe_allow_html=True)
k4.markdown(f'<div class="kpi"><span class="kpi-label">Network Mean Days</span><span class="kpi-value">{df["Days Left"].mean():.1f}d</span><span class="kpi-delta-pos">{surp_count} Donors</span></div>', unsafe_allow_html=True)

# =============================================================================
# §5  GEOSPATIAL VECTORS (FOLIUM MAP) & TABLE
# =============================================================================
st.markdown('<div class="sec">Geospatial Distribution & Depletion Matrix</div>', unsafe_allow_html=True)
col_map, col_tbl = st.columns([1.5, 1.3])

with col_map:
    m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=12, tiles="OpenStreetMap")
    for _, row in df.iterrows():
        color = URGENCY_HEX.get(row["Urgency"], "#28c76f")
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]], radius=8, color=color, fill=True, fill_color=color, fill_opacity=0.85,
            popup=f"<b>{row['Hospital Name']}</b><br>Stock: {int(row['Current Medicine Stock'])}<br>Days Left: {row['Days Left']}d"
        ).add_to(m)
        
    if st.session_state["active"] and routes:
        for r in routes:
            folium.PolyLine(
                locations=[[r["from_lat"], r["from_lon"]], [r["to_lat"], r["to_lon"]]],
                color="#0066FF", weight=4, opacity=0.9, dash_array="6, 8",
                tooltip=f"Route: {r['Origin']} ➔ {r['Destination']} | {r['Allocated Units']} units"
            ).add_to(m)
    st_folium(m, height=450, width="100%")

with col_tbl:
    disp_df = df[["Hospital Name", "Current Medicine Stock", "Days Left", "Urgency", "Severity Index"]].copy()
    st.dataframe(disp_df, height=450, use_container_width=True)

# =============================================================================
# §6  COMPARATIVE STOCK ANALYTICS (CHARTS) 
# =============================================================================
st.markdown('<div class="sec">Comparative Stock Analytics</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns(2)

with ch1:
    st.markdown("**Current vs. Projected Stock**")
    chart_df = df[df["Urgency"].isin(["Critical", "Imminent"])][["Hospital Name", "Current Medicine Stock", "Projected Stock"]]
    if not chart_df.empty:
        st.bar_chart(chart_df.set_index("Hospital Name"))
    else:
        st.info("Trigger a reroute to see stock redistribution here.")

with ch2:
    st.markdown("**Node Status Distribution**")
    st.bar_chart(df["Urgency"].value_counts())

# =============================================================================
# §7  POST-REROUTE ANALYTICS & DIRECTIVES
# =============================================================================
if st.session_state["active"]:
    st.markdown('<div class="sec">Post-Reroute Operational Telemetry & Directives</div>', unsafe_allow_html=True)
    if routes:
        tot_orders, tot_units = len(routes), sum(r["Allocated Units"] for r in routes)
        tot_dist = round(sum(r["Road Distance (km)"] for r in routes), 1)
        tot_cost = round(sum(r["Cost (INR)"] for r in routes), 0)
        tot_co2 = round(sum(r["CO2 (kg)"] for r in routes), 2)
        
        t1, t2, t3, t4, t5 = st.columns(5)
        t1.markdown(f'<div class="tele"><div class="tele-val">{tot_orders}</div><div class="tele-lbl">Orders</div></div>', unsafe_allow_html=True)
        t2.markdown(f'<div class="tele"><div class="tele-val">{tot_units}</div><div class="tele-lbl">Units Mobilized</div></div>', unsafe_allow_html=True)
        t3.markdown(f'<div class="tele"><div class="tele-val">{tot_dist} km</div><div class="tele-lbl">Road Distance</div></div>', unsafe_allow_html=True)
        t4.markdown(f'<div class="tele"><div class="tele-val">₹{tot_cost:,.0f}</div><div class="tele-lbl">Transport Cost</div></div>', unsafe_allow_html=True)
        t5.markdown(f'<div class="tele"><div class="tele-val">{tot_co2} kg</div><div class="tele-lbl">CO2 Impact</div></div>', unsafe_allow_html=True)
        
        st.dataframe(pd.DataFrame(routes)[["Origin", "Destination", "Allocated Units", "Road Distance (km)", "Transit Time (hrs)", "Vehicle Type", "Cost (INR)"]], use_container_width=True)
    else:
        st.info("No rerouting required — all facilities meet minimum reserve criteria.")