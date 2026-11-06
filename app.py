import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(
    page_title="AeroFlame_Analytics",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

pages = ["Home", "Explorer", "Charts", "What-If", "Documents", "Basics", "About"]
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

bg_color = "#0E1A2B"
card_bg = "linear-gradient(145deg, #162238 0%, #121C2F 100%)"
card_bg_flat = "#162238"
card_border = "#24344D"
text_color = "#EAF0FA"
header_color = "#FFFFFF"
sub_text = "#94A3B8"
nav_bg = "#121E31"
btn_sec_bg = "#162238"
btn_sec_border = "#24344D"
btn_sec_text = "#EAF0FA"
plotly_template = "plotly_dark"
chart_point_color = "#4C8BF5"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
}}
header[data-testid="stHeader"] {{
    display: none !important;
    height: 0 !important;
    pointer-events: none !important;
}}
.block-container {{
    padding-top: 1.25rem !important;
    padding-bottom: 2.5rem !important;
    padding-left: 24px !important;
    padding-right: 24px !important;
    max-width: 100% !important;
}}
.stApp {{
    background-color: {bg_color};
    color: {text_color};
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif;
    font-size: 15px;
    line-height: 1.65;
    font-weight: 400;
}}
h1, h2, h3, h4, h5, h6 {{
    color: {header_color} !important;
    font-family: 'Space Grotesk', 'Segoe UI', Arial, sans-serif !important;
    font-weight: 600;
    letter-spacing: -0.015em;
}}
p, span, label, div {{
    color: {text_color};
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif;
}}
input, textarea, select, [data-baseweb] {{
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif !important;
    font-size: 15px !important;
}}
.stMarkdown, .stExpander, [data-testid="stTable"] {{
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child {{
    background: #121E31;
    border-radius: 16px;
    padding: 24px 18px;
    border: 1px solid #24344D;
    position: sticky;
    top: 1.25rem;
    height: fit-content;
    min-width: 255px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}}
.stButton {{
    width: 100% !important;
}}
.stButton > button {{
    width: 100% !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    position: relative !important;
    z-index: 10 !important;
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    margin-bottom: 6px !important;
}}
.stButton button * {{
    pointer-events: none !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child .stButton {{
    width: 100% !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child .stButton > button {{
    width: 100% !important;
    min-height: 44px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    position: relative !important;
    z-index: 10 !important;
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 12px 16px !important;
    margin-bottom: 8px !important;
    border-radius: 12px !important;
    border: 1px solid #24344D !important;
    background: #162238 !important;
    color: #EAF0FA !important;
    box-shadow: none !important;
    transition: all 0.2s ease-in-out !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child .stButton > button:hover {{
    transform: translateY(-2px) !important;
    border-color: #FF6A00 !important;
    color: #FF6A00 !important;
    box-shadow: 0 4px 14px rgba(255, 106, 0, 0.15) !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child .stButton > button[kind="primary"] {{
    background-color: #FF6A00 !important;
    color: #FFFFFF !important;
    border: 1px solid #FF6A00 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(255, 106, 0, 0.35) !important;
}}
div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"]:first-child .stButton > button[kind="primary"]:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(255, 106, 0, 0.5) !important;
    color: #FFFFFF !important;
    border-color: #FF6A00 !important;
}}
button[kind="primary"] {{
    background-color: #FF6A00 !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 14px rgba(255, 106, 0, 0.35) !important;
    transition: all 0.2s ease-in-out !important;
}}
button[kind="primary"]:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(255, 106, 0, 0.5) !important;
}}
button[kind="secondary"] {{
    background: {btn_sec_bg} !important;
    color: {btn_sec_text} !important;
    border: 1px solid {btn_sec_border} !important;
    font-weight: 500 !important;
    border-radius: 12px !important;
    transition: all 0.2s ease-in-out !important;
}}
button[kind="secondary"]:hover {{
    transform: translateY(-2px) !important;
    border-color: #FF6A00 !important;
    color: #FF6A00 !important;
    box-shadow: 0 4px 14px rgba(255, 106, 0, 0.15) !important;
}}
div[data-baseweb="slider"] div[role="slider"] {{
    background-color: #FF6A00 !important;
    border-color: #FF6A00 !important;
}}
div[data-baseweb="slider"] div {{
    background: #FF6A00 !important;
}}
.hero-banner {{
    background: linear-gradient(135deg, #0B3D91 0%, #061F4F 100%);
    border-radius: 16px;
    padding: 36px 40px;
    margin-bottom: 32px;
    color: #FFFFFF;
    box-shadow: 0 8px 24px rgba(11, 61, 145, 0.25);
}}
.badge-orange {{
    background-color: #FF6A00;
    color: #FFFFFF !important;
    padding: 5px 14px;
    border-radius: 20px;
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.1em;
    display: inline-block;
    margin-bottom: 12px;
}}
.hero-title {{
    color: #FFFFFF !important;
    font-family: 'Space Grotesk', 'Segoe UI', Arial, sans-serif !important;
    font-size: 44px;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin: 0;
}}
.hero-subtitle {{
    color: #FF6A00 !important;
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif;
    font-size: 18px;
    font-weight: 400;
    margin-top: 10px;
}}
.metric-card {{
    background: {card_bg};
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    border: 1px solid {card_border};
    margin-bottom: 20px;
    transition: transform 0.2s ease-in-out;
}}
.metric-card:hover {{
    transform: translateY(-3px);
}}
.metric-label {{
    color: {sub_text} !important;
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif;
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}
.metric-value {{
    color: {text_color} !important;
    font-family: 'Space Grotesk', 'Segoe UI', Arial, sans-serif;
    font-size: 30px;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
    margin-top: 4px;
}}
.info-card {{
    background: {card_bg};
    border-radius: 16px;
    padding: 24px 26px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    border: 1px solid {card_border};
    margin-bottom: 20px;
    height: 100%;
}}
.info-title {{
    color: {header_color} !important;
    font-family: 'Space Grotesk', 'Segoe UI', Arial, sans-serif !important;
    font-size: 19px;
    font-weight: 600;
    letter-spacing: -0.015em;
    margin-bottom: 10px;
}}
.what-if-box {{
    background: {card_bg};
    border-radius: 16px;
    padding: 22px 26px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    border: 1px solid {card_border};
    margin-top: 16px;
    margin-bottom: 28px;
}}
.risk-badge {{
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif;
    font-size: 18px;
    font-weight: 500;
    letter-spacing: 0.1em;
    color: #FFFFFF !important;
    margin-bottom: 8px;
}}
.step-card {{
    background: {card_bg};
    border-radius: 16px;
    padding: 20px 22px;
    border: 1px solid {card_border};
    text-align: center;
}}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=60)
def fetch_api(endpoint):
    try:
        res = requests.get(f"http://127.0.0.1:8000{endpoint}", timeout=5)
        if res.status_code == 200:
            return res.json()
        return None
    except Exception:
        return None

health_status = fetch_api("/health")
if not health_status:
    st.markdown("""
    <div style="background-color: #FF6A00; color: white; padding: 24px 30px; border-radius: 16px; margin: 30px auto; max-width: 800px; box-shadow: 0 8px 24px rgba(255,106,0,0.3);">
        <h2 style="color: white !important; margin: 0 0 10px 0;">FastAPI Backend Offline</h2>
        <p style="color: white !important; font-size: 16px; margin-bottom: 14px;">The dashboard requires the local FastAPI database server running at <code>http://127.0.0.1:8000</code>.</p>
        <p style="color: white !important; font-size: 15px; margin: 0;">Please run this command in a terminal:</p>
        <div style="background: rgba(0,0,0,0.25); padding: 12px 18px; border-radius: 8px; font-family: monospace; font-size: 16px; margin-top: 8px;">
            python -m uvicorn main:app --reload
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

def normalize_fuel(val):
    if not val:
        return "Not Specified"
    s = re.sub(r"\s+", " ", str(val).strip())
    s = re.sub(r"%\s*([a-zA-Z0-9])", r"% \1", s)
    return s

col_sidebar, col_main = st.columns([1.25, 5.75], gap="medium")

with col_sidebar:
    st.markdown("""
    <div style="padding: 4px 0 20px 0; white-space: nowrap;">
        <span style="font-size: 18px; font-weight: 800; color: #FF6A00; white-space: nowrap; letter-spacing: -0.01em;">🔥 AeroFlame_Analytics</span>
    </div>
    """, unsafe_allow_html=True)

    for p_name in pages:
        is_active = (st.session_state.current_page == p_name)
        btn_type = "primary" if is_active else "secondary"
        if st.button(p_name, key=f"side_nav_{p_name}", type=btn_type, use_container_width=True):
            st.session_state.current_page = p_name
            st.rerun()

with col_main:
    experiments_data = fetch_api("/api/experiments?limit=500") or []

    if st.session_state.current_page == "Home":
        st.markdown("""
        <div class="hero-banner">
            <h1 class="hero-title">AeroFlame_Analytics</h1>
            <div class="hero-subtitle">SI-Powered Fire Safety Insights from Microgravity Combustion Data</div>
            <div style="margin-top: 22px;">
        """, unsafe_allow_html=True)

        if st.button("Start Exploring", key="hero_cta", type="primary"):
            st.session_state.current_page = "Explorer"
            st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)

        total_tests = len(experiments_data)
        total_flames = int(sum(float(r.get("flames_ignited") or 0) for r in experiments_data))
        all_ox = [lvl for r in experiments_data for lvl in r.get("oxygen_levels", [])]
        avg_ox_str = f"{sum(all_ox)/len(all_ox):.1f}%" if all_ox else "N/A"
        unique_fuels = sorted(list({normalize_fuel(r.get("fuel_bottle")) for r in experiments_data if r.get("fuel_bottle")}))

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Experiments</div>
                <div class="metric-value">{total_tests} Tests</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Flames Caught Fire</div>
                <div class="metric-value">{total_flames} Ignitions</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Average Oxygen Level</div>
                <div class="metric-value">{avg_ox_str}</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Fuel Mixtures Tested</div>
                <div class="metric-value">{len(unique_fuels)} Types</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<h2 style='margin: 32px 0 16px 0;'>Mission Insights</h2>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">Spherical Flame Physics</div>
                <div>Without buoyancy-driven convection, flames become spherical, burning cooler and dimmer, relying solely on slow molecular diffusion.</div>
                <div style="margin-top: 16px;">
            """, unsafe_allow_html=True)
            if st.button("Explore Flame Basics →", key="feat_btn_basics", type="secondary", use_container_width=True):
                st.session_state.current_page = "Basics"
                st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)

        with f2:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">Habitat Fire Safety</div>
                <div>Future Artemis Moon and Mars crew habitats utilize elevated oxygen environments that significantly heighten ignition sensitivity.</div>
                <div style="margin-top: 16px;">
            """, unsafe_allow_html=True)
            if st.button("Simulate What-If Risks →", key="feat_btn_whatif", type="secondary", use_container_width=True):
                st.session_state.current_page = "What-If"
                st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)

        with f3:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">Suppression Strategy</div>
                <div>Extinguishing microgravity fire requires understanding forced cabin airflow dynamics and gaseous suppressant distribution.</div>
                <div style="margin-top: 16px;">
            """, unsafe_allow_html=True)
            if st.button("View Analytics Charts →", key="feat_btn_charts", type="secondary", use_container_width=True):
                st.session_state.current_page = "Charts"
                st.rerun()
            st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("<h2 style='margin: 32px 0 16px 0;'>How to Use This Dashboard</h2>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown("""
            <div class="step-card">
                <div style="font-size: 28px; font-weight: 800; color: #FF6A00; margin-bottom: 6px;">01</div>
                <div style="font-weight: 700; margin-bottom: 4px;">Filter Combustion Records</div>
                <div style="font-size: 14px; color: #94A3B8;">Navigate to Explorer to filter tests by oxygen dilution, fuel bottle, and burner size.</div>
            </div>
            """, unsafe_allow_html=True)
        with s2:
            st.markdown("""
            <div class="step-card">
                <div style="font-size: 28px; font-weight: 800; color: #FF6A00; margin-bottom: 6px;">02</div>
                <div style="font-weight: 700; margin-bottom: 4px;">Simulate Environmental Risk</div>
                <div style="font-size: 14px; color: #94A3B8;">Adjust the What-If slider to evaluate cabin flammability hazards and see nearest NASA tests.</div>
            </div>
            """, unsafe_allow_html=True)
        with s3:
            st.markdown("""
            <div class="step-card">
                <div style="font-size: 28px; font-weight: 800; color: #FF6A00; margin-bottom: 6px;">03</div>
                <div style="font-weight: 700; margin-bottom: 4px;">Inspect Technical Papers</div>
                <div style="font-size: 14px; color: #94A3B8;">Read extracted executive summaries of NASA research papers and review the 22 flight datasets.</div>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.current_page == "Explorer":
        st.markdown("<h2>Experiments Explorer</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 20px;'>Filter, sort, and inspect microgravity combustion tests cataloged from NASA PSI flight archives.</p>", unsafe_allow_html=True)

        fuel_names_set = sorted(list({normalize_fuel(r.get("fuel_bottle")) for r in experiments_data if r.get("fuel_bottle")}))

        fc1, fc2, fc3, fc4 = st.columns([1.5, 1.5, 1.2, 1.5])
        with fc1:
            ox_range = st.slider("Oxygen Range (%)", min_value=21.0, max_value=40.0, value=(21.0, 40.0), step=0.5)
        with fc2:
            selected_fuels = st.multiselect("Fuel Bottle", fuel_names_set, default=fuel_names_set)
        with fc3:
            max_possible_flames = max([float(r.get("flames_ignited") or 0) for r in experiments_data] or [10.0])
            min_flames = st.slider("Min Flames Ignited", 0.0, float(max_possible_flames), 0.0, step=1.0)
        with fc4:
            search_query = st.text_input("Search Notes", placeholder="e.g. pressure, ISS, dilution...")

        filtered_records = []
        for r in experiments_data:
            norm_f = normalize_fuel(r.get("fuel_bottle"))
            if selected_fuels and (norm_f not in selected_fuels):
                continue
            flames_val = float(r.get("flames_ignited") or 0)
            if flames_val < min_flames:
                continue
            levels = r.get("oxygen_levels", [])
            if levels and not any(ox_range[0] <= lvl <= ox_range[1] for lvl in levels):
                continue
            if search_query:
                notes_str = str(r.get("notes") or "").lower()
                if search_query.lower() not in notes_str:
                    continue
            filtered_records.append(r)

        f_cnt = len(filtered_records)
        f_flames = int(sum(float(r.get("flames_ignited") or 0) for r in filtered_records))
        f_ox_list = [lvl for r in filtered_records for lvl in r.get("oxygen_levels", []) if ox_range[0] <= lvl <= ox_range[1]]
        f_avg_ox = f"{sum(f_ox_list)/len(f_ox_list):.1f}%" if f_ox_list else "N/A"

        sm1, sm2, sm3 = st.columns(3)
        with sm1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Matching Experiments</div>
                <div class="metric-value">{f_cnt}</div>
            </div>
            """, unsafe_allow_html=True)
        with sm2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Flames Ignited</div>
                <div class="metric-value">{f_flames}</div>
            </div>
            """, unsafe_allow_html=True)
        with sm3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Filtered Avg Oxygen</div>
                <div class="metric-value">{f_avg_ox}</div>
            </div>
            """, unsafe_allow_html=True)

        table_rows = []
        for r in filtered_records:
            levels_str = ", ".join(f"{x:g}%" for x in r.get("oxygen_levels", [])) if r.get("oxygen_levels") else "N/A"
            notes_full = r.get("notes") or ""
            notes_prev = (str(notes_full)[:60] + "...") if len(str(notes_full)) > 60 else str(notes_full)
            flames_num = int(r.get("flames_ignited")) if r.get("flames_ignited") is not None else 0
            table_rows.append({
                "Year": int(r.get("year")) if r.get("year") else "",
                "Month": r.get("month") or "",
                "Date": r.get("date") or "",
                "Burner size (mm)": r.get("burner_size_(mm)") or "",
                "Fuel": normalize_fuel(r.get("fuel_bottle")),
                "Oxygen levels": levels_str,
                "Flames that caught fire": flames_num,
                "Notes preview": notes_prev,
                "Full Notes": notes_full
            })

        if table_rows:
            df_table = pd.DataFrame(table_rows)
            display_df = df_table.drop(columns=["Full Notes"])

            st.dataframe(
                display_df,
                column_config={
                    "Flames that caught fire": st.column_config.ProgressColumn(
                        "Flames that caught fire",
                        help="Total number of ignited flames",
                        format="%d",
                        min_value=0,
                        max_value=int(max_possible_flames) or 10
                    )
                },
                use_container_width=True,
                hide_index=True
            )

            csv_bytes = display_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Filtered Table (CSV)",
                data=csv_bytes,
                file_name="flame_experiments_filtered.csv",
                mime="text/csv",
                type="primary"
            )

            with st.expander("Open Full Notes Inspector"):
                row_labels = [
                    f"Row {i+1}: {r['Date']} {r['Month']} {r['Year']} | Fuel: {r['Fuel']} | Flames: {r['Flames that caught fire']}"
                    for i, r in enumerate(table_rows)
                ]
                sel_idx = st.selectbox("Select an experiment to read complete technician log:", range(len(row_labels)), format_func=lambda x: row_labels[x])
                st.markdown(f"**Full Notes for Row {sel_idx+1}:**")
                st.info(table_rows[sel_idx]["Full Notes"] or "No notes logged for this experiment run.")
        else:
            st.info("No experiment rows match your active filter criteria.")

    elif st.session_state.current_page == "Charts":
        st.markdown("<h2>Interactive Visual Analytics</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 24px;'>Explore correlations between oxygen concentration, fuel mixtures, and flame ignition events.</p>", unsafe_allow_html=True)

        scatter_pts = []
        for r in experiments_data:
            flames = r.get("flames_ignited")
            fuel = normalize_fuel(r.get("fuel_bottle"))
            notes_snippet = (str(r.get("notes"))[:80] + "...") if r.get("notes") else "None"
            date_lbl = f"{r.get('month', '')} {r.get('date', '')}, {int(r.get('year', 0)) if r.get('year') else ''}"
            for lvl in r.get("oxygen_levels", []):
                scatter_pts.append({
                    "Oxygen (%)": lvl,
                    "Flames Caught Fire": flames,
                    "Fuel": fuel,
                    "Date": date_lbl,
                    "Notes": notes_snippet
                })

        col_chart_left, col_chart_right = st.columns(2)

        with col_chart_left:
            st.markdown("#### Oxygen % vs Flames Caught Fire")
            fuel_highlight_options = ["All"] + sorted(list({p["Fuel"] for p in scatter_pts}))
            highlight_fuel = st.selectbox("Highlight Fuel Type", fuel_highlight_options, key="chart_fuel_hl")

            if scatter_pts:
                df_sc = pd.DataFrame(scatter_pts)
                fig_sc = go.Figure()

                if highlight_fuel == "All":
                    fig_sc.add_trace(go.Scatter(
                        x=df_sc["Oxygen (%)"],
                        y=df_sc["Flames Caught Fire"],
                        mode="markers",
                        name="Experiments",
                        marker=dict(size=11, color=chart_point_color, line=dict(width=1, color="#FFFFFF")),
                        customdata=df_sc[["Fuel", "Date", "Notes"]],
                        hovertemplate="<b>Oxygen:</b> %{x}%<br><b>Flames:</b> %{y}<br><b>Fuel:</b> %{customdata[0]}<br><b>Date:</b> %{customdata[1]}<br><b>Notes:</b> %{customdata[2]}<extra></extra>"
                    ))
                else:
                    df_other = df_sc[df_sc["Fuel"] != highlight_fuel]
                    df_hl = df_sc[df_sc["Fuel"] == highlight_fuel]

                    if not df_other.empty:
                        fig_sc.add_trace(go.Scatter(
                            x=df_other["Oxygen (%)"],
                            y=df_other["Flames Caught Fire"],
                            mode="markers",
                            name="Other Fuels",
                            marker=dict(size=9, color="#94A3B8", opacity=0.45, line=dict(width=1, color="#FFFFFF")),
                            customdata=df_other[["Fuel", "Date", "Notes"]],
                            hovertemplate="<b>Oxygen:</b> %{x}%<br><b>Flames:</b> %{y}<br><b>Fuel:</b> %{customdata[0]}<br><b>Date:</b> %{customdata[1]}<extra></extra>"
                        ))
                    if not df_hl.empty:
                        fig_sc.add_trace(go.Scatter(
                            x=df_hl["Oxygen (%)"],
                            y=df_hl["Flames Caught Fire"],
                            mode="markers",
                            name=f"Highlighted: {highlight_fuel}",
                            marker=dict(size=14, color="#FF6A00", symbol="diamond", line=dict(width=2, color="#FFFFFF")),
                            customdata=df_hl[["Fuel", "Date", "Notes"]],
                            hovertemplate="<b>%{customdata[0]}</b><br><b>Oxygen:</b> %{x}%<br><b>Flames:</b> %{y}<br><b>Date:</b> %{customdata[1]}<br><b>Notes:</b> %{customdata[2]}<extra></extra>"
                        ))

                fig_sc.update_layout(
                    template=plotly_template,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis_title="Oxygen Concentration (%)",
                    yaxis_title="Flames Caught Fire",
                    font=dict(family="DM Sans, Arial, sans-serif", color="#EAF0FA"),
                    xaxis_title_font=dict(family="DM Sans, Arial, sans-serif"),
                    yaxis_title_font=dict(family="DM Sans, Arial, sans-serif"),
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=420,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig_sc, use_container_width=True)
            else:
                st.info("No scatter plot data points available.")

        with col_chart_right:
            st.markdown("#### Fuel Bottle Distribution")
            bar_metric = st.radio("Bar Chart Metric", ["Experiment Count", "Total Flames Ignited"], horizontal=True, key="bar_metric_toggle")

            fuel_rows = []
            for r in experiments_data:
                fuel_rows.append({
                    "Fuel": normalize_fuel(r.get("fuel_bottle")),
                    "Flames": float(r.get("flames_ignited") or 0)
                })

            if fuel_rows:
                df_fb = pd.DataFrame(fuel_rows)
                if bar_metric == "Experiment Count":
                    df_bar = df_fb["Fuel"].value_counts().reset_index()
                    df_bar.columns = ["Fuel", "Value"]
                    y_label = "Experiment Count"
                else:
                    df_bar = df_fb.groupby("Fuel", as_index=False)["Flames"].sum()
                    df_bar.columns = ["Fuel", "Value"]
                    y_label = "Total Flames Ignited"

                fig_bar = px.bar(
                    df_bar,
                    x="Fuel",
                    y="Value",
                    text="Value",
                    template=plotly_template,
                    color_discrete_sequence=[chart_point_color]
                )
                fig_bar.update_traces(textposition="outside", marker_line_color="#FFFFFF", marker_line_width=1)
                fig_bar.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis_title="Fuel Mixture",
                    yaxis_title=y_label,
                    font=dict(family="DM Sans, Arial, sans-serif", color="#EAF0FA"),
                    xaxis_title_font=dict(family="DM Sans, Arial, sans-serif"),
                    yaxis_title_font=dict(family="DM Sans, Arial, sans-serif"),
                    margin=dict(l=20, r=20, t=30, b=20),
                    height=420
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No fuel distribution records available.")

    elif st.session_state.current_page == "What-If":
        st.markdown("<h2>What-If Combustion Risk Simulator</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 24px;'>Simulate how altering habitat oxygen levels impacts ignition hazard and review nearest past NASA experiments.</p>", unsafe_allow_html=True)

        sim_ox = st.slider("Select What-If Oxygen Concentration (%)", min_value=21.0, max_value=40.0, value=25.0, step=0.5)

        if sim_ox < 23.0:
            badge_bg = "#10B981"
            badge_txt = "Low risk"
            explanation = "Oxygen concentration is within nominal Earth-normal baseline, minimizing spontaneous combustion and rapid flame acceleration."
        elif sim_ox <= 30.0:
            badge_bg = "#F59E0B"
            badge_txt = "Medium risk"
            explanation = "Elevated oxygen noticeably lowers ignition energy requirements and increases microgravity flame propagation speed."
        else:
            badge_bg = "#EF4444"
            badge_txt = "High risk"
            explanation = "Oxygen-enriched environment creates severe fire hazard, allowing materials that resist ignition in air to burn vigorously."

        st.markdown(f"""
        <div class="what-if-box" style="border-left: 6px solid {badge_bg};">
            <span class="risk-badge" style="background-color: {badge_bg};">{badge_txt} at {sim_ox}% O₂</span>
            <div class="risk-desc" style="font-size: 16px; font-weight: 500; margin-top: 6px;">{explanation}</div>
        </div>
        """, unsafe_allow_html=True)

        scatter_all = []
        for r in experiments_data:
            flames = r.get("flames_ignited")
            fuel = normalize_fuel(r.get("fuel_bottle"))
            notes_str = (str(r.get("notes"))[:60] + "...") if r.get("notes") else "None"
            date_lbl = f"{r.get('month', '')} {r.get('date', '')}, {int(r.get('year', 0)) if r.get('year') else ''}"
            for lvl in r.get("oxygen_levels", []):
                scatter_all.append({
                    "Oxygen (%)": lvl,
                    "Flames Caught Fire": flames,
                    "Fuel": fuel,
                    "Date": date_lbl,
                    "Notes": notes_str,
                    "RawRow": r
                })

        if scatter_all:
            df_sim = pd.DataFrame(scatter_all)
            fig_sim = go.Figure()

            fig_sim.add_trace(go.Scatter(
                x=df_sim["Oxygen (%)"],
                y=df_sim["Flames Caught Fire"],
                mode="markers",
                name="NASA Flight Data",
                marker=dict(size=10, color=chart_point_color, opacity=0.7, line=dict(width=1, color="#FFFFFF")),
                customdata=df_sim[["Fuel", "Date", "Notes"]],
                hovertemplate="<b>Oxygen:</b> %{x}%<br><b>Flames:</b> %{y}<br><b>Fuel:</b> %{customdata[0]}<br><b>Date:</b> %{customdata[1]}<extra></extra>"
            ))

            fig_sim.add_vline(
                x=sim_ox,
                line_width=2.5,
                line_dash="dash",
                line_color="#FF6A00",
                annotation_text=f"Selected What-If ({sim_ox}%)",
                annotation_position="top right"
            )

            matched_pts = df_sim[df_sim["Oxygen (%)"] == sim_ox]
            if not matched_pts.empty:
                fig_sim.add_trace(go.Scatter(
                    x=matched_pts["Oxygen (%)"],
                    y=matched_pts["Flames Caught Fire"],
                    mode="markers",
                    name="Exact Match Point",
                    marker=dict(size=15, color="#FF6A00", symbol="diamond", line=dict(width=2, color="#FFFFFF")),
                    customdata=matched_pts[["Fuel", "Date", "Notes"]],
                    hovertemplate="<b>Exact Match!</b><br><b>Oxygen:</b> %{x}%<br><b>Flames:</b> %{y}<br><b>Fuel:</b> %{customdata[0]}<extra></extra>"
                ))

            fig_sim.update_layout(
                template=plotly_template,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Oxygen Concentration (%)",
                yaxis_title="Flames Caught Fire",
                margin=dict(l=20, r=20, t=30, b=20),
                height=380
            )
            st.plotly_chart(fig_sim, use_container_width=True)

        st.markdown("<h3 style='margin: 32px 0 16px 0;'>Nearest Past NASA Experiments (Within ±1.5% O₂)</h3>", unsafe_allow_html=True)

        with_delta = []
        for item in scatter_all:
            diff = abs(item["Oxygen (%)"] - sim_ox)
            if diff <= 1.5:
                with_delta.append((diff, item))

        with_delta.sort(key=lambda x: x[0])
        top_5 = with_delta[:5]

        if top_5:
            near_cols = st.columns(min(len(top_5), 5))
            for col, (diff, item) in zip(near_cols, top_5):
                with col:
                    st.markdown(f"""
                    <div class="info-card" style="padding: 16px 18px;">
                        <div style="color: #FF6A00; font-size: 13px; font-weight: 700;">Δ {diff:.1f}% from Target</div>
                        <div style="font-size: 20px; font-weight: 800; margin: 4px 0;">{item['Oxygen (%)']}% O₂</div>
                        <div style="font-size: 13px;"><b>Fuel:</b> {item['Fuel']}</div>
                        <div style="font-size: 13px;"><b>Flames:</b> {int(item['Flames Caught Fire']) if item['Flames Caught Fire'] else 0}</div>
                        <div style="font-size: 12px; color: #94A3B8; margin-top: 6px;">{item['Date']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info(f"No flight experiments found in the archive within ±1.5% of {sim_ox}% oxygen.")

    elif st.session_state.current_page == "Documents":
        st.markdown("<h2>NASA Documents and Flight Files</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 24px;'>Access extracted research papers from the NASA Technical Reports Server (NTRS) and Physical Sciences Informatics (PSI).</p>", unsafe_allow_html=True)

        docs_all = fetch_api("/api/documents") or []
        files_all = fetch_api("/api/files") or []

        doc_search = st.text_input("Search Research Documents", placeholder="Filter by title, keywords, or source folder...")

        filtered_docs = []
        for d in docs_all:
            txt = (str(d.get("title") or "") + " " + str(d.get("source_folder") or "") + " " + str(d.get("text") or "")).lower()
            if not doc_search or doc_search.lower() in txt:
                filtered_docs.append(d)

        st.markdown(f"<h3 style='margin: 20px 0 12px 0;'>Cataloged Papers & Reports ({len(filtered_docs)} Documents)</h3>", unsafe_allow_html=True)
        for doc in filtered_docs:
            with st.expander(f"{doc.get('title')} ({doc.get('source_folder')}) — {doc.get('page_count')} Pages"):
                st.markdown(f"**Source Repository:** `{doc.get('source_folder')}` | **Page Count:** `{doc.get('page_count')}`")
                st.markdown("**Executive Excerpt:**")
                st.write(doc.get("text") or "No text excerpt available.")

        st.markdown("<h3 style='margin: 36px 0 16px 0;'>Source Files Inventory (22 Dataset Files)</h3>", unsafe_allow_html=True)

        ext_options = ["All"] + sorted(list({f.get("type") for f in files_all if f.get("type")}))
        selected_ext = st.selectbox("Filter by File Extension", ext_options)

        filtered_f = [f for f in files_all if selected_ext == "All" or f.get("type") == selected_ext]

        if filtered_f:
            df_f = pd.DataFrame(filtered_f)
            df_f.rename(columns={
                "file_id": "File ID",
                "path": "Relative File Path",
                "type": "Extension",
                "source_folder": "Repository",
                "investigation": "Investigation"
            }, inplace=True)
            st.dataframe(df_f, use_container_width=True, hide_index=True)
        else:
            st.info("No files matching the selected extension.")

    elif st.session_state.current_page == "Basics":
        st.markdown("<h2>Microgravity Combustion Science Basics</h2>", unsafe_allow_html=True)
        st.markdown("<p style='margin-bottom: 28px;'>Fundamental physics of combustion in freefall and extraterrestrial environments.</p>", unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        with b1:
            st.markdown("""
            <div class="info-card">
                <div>
                    <div class="info-title">1-g Flame (Earth Atmosphere)</div>
                    <p><strong>Geometry:</strong> Familiar teardrop / elongated cone shape.</p>
                    <p><strong>Mechanism:</strong> Hot combustion gases have lower density than cold ambient air, creating strong buoyancy-driven upward convective draft.</p>
                    <p><strong>Oxygen Supply:</strong> Natural draft continuously draws fresh oxygen into the base of the reaction zone.</p>
                    <p><strong>Soot Dynamics:</strong> Soot is swept rapidly upward into the hot flame tip, burning to produce characteristic yellow incandescent light.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with b2:
            st.markdown("""
            <div class="info-card">
                <div>
                    <div class="info-title">0-g Flame (Spacecraft Microgravity)</div>
                    <p><strong>Geometry:</strong> Symmetrical hemispherical or perfectly spherical ball.</p>
                    <p><strong>Mechanism:</strong> Buoyancy forces vanish in freefall; hot gases expand equally in all 3D directions without rising.</p>
                    <p><strong>Oxygen Supply:</strong> Oxygen moves into the flame purely via molecular diffusion or forced HVAC cabin circulation, burning cooler and dimmer (blue flame).</p>
                    <p><strong>Soot Dynamics:</strong> Soot particles accumulate in a spherical shell, radiating heat outward and increasing extinction vulnerability.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<h3 style='margin: 32px 0 16px 0;'>Partial Gravity: Moon (1/6-g) and Mars (1/3-g)</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="info-card">
            In partial gravity, buoyant convection is too weak to create vigorous upward draft like Earth, but strong enough to supply continuous fresh oxygen without diffusion starvation. Research from NASA LUCI and FM2 projects indicates that partial gravity environments can sustain flammability at lower oxygen levels than either 0-g or 1-g!
        </div>
        """, unsafe_allow_html=True)

        p_ox, p_flam = st.columns(2)
        with p_ox:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">Why Oxygen Matters</div>
                <div>Cabin oxygen concentration dictates both ignition energy and burning velocity. A shift from 21% to 30% O2 increases flame spread rates dramatically, turning fire-retardant materials into active hazards.</div>
            </div>
            """, unsafe_allow_html=True)
        with p_flam:
            st.markdown("""
            <div class="info-card">
                <div class="info-title">What Flammability Means</div>
                <div>Flammability in spaceflight is defined by the Limiting Oxygen Concentration (LOC) and maximum spread rate before radiative quenching causes flame extinction.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<h3 style='margin: 32px 0 16px 0;'>Key NASA Flight Investigations</h3>", unsafe_allow_html=True)
        inv1, inv2, inv3 = st.columns(3)
        with inv1:
            with st.expander("SAFFIRE (I - VI)"):
                st.markdown("**Spacecraft Fire Safety:** Performed inside uncrewed Cygnus resupply spacecraft after departing ISS. Studied large-scale fabric and PMMA panel burns up to 1 meter in length.")
        with inv2:
            with st.expander("ACME BRE"):
                st.markdown("**Burning Rate Emulator:** Evaluated gaseous hydrocarbon fuels (Ethylene/Nitrogen) to mimic solid fuel burning rates under varying oxygen enrichment on the ISS.")
        with inv3:
            with st.expander("BASS-II"):
                st.markdown("**Burning & Suppression of Solids:** Conducted in the Microgravity Science Glovebox on ISS, determining exact inert gas extinction thresholds for polymeric rods.")

        with st.expander("Combustion Science Glossary"):
            st.markdown("""
            - **Microgravity (0-g):** Condition of freefall where apparent gravitational acceleration is near zero.
            - **Buoyancy:** Upward force exerted by a fluid that opposes the weight of an immersed object due to density differentials.
            - **Molecular Diffusion:** Thermal motion of particles causing net movement from high concentration to low concentration.
            - **Quenching:** Extinction of a flame when heat losses exceed heat generated by combustion reactions.
            - **Limiting Oxygen Concentration (LOC):** Minimum oxygen percentage supporting self-sustained flame propagation.
            """)

    elif st.session_state.current_page == "About":
        st.markdown("<h2>About This Project</h2>", unsafe_allow_html=True)

        st.markdown("""
        <div class="hero-banner">
            <h2 style="color:white !important; margin:0 0 6px 0;">AeroFlame_Analytics</h2>
            <div style="color:#FF6A00; font-size:17px; font-weight:600;">SI-Powered Fire Safety Insights from Microgravity Combustion Data</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Project Purpose")
        st.markdown("""
        This prototype analyzes microgravity combustion experiments and technical literature from NASA spaceflight investigations to:
        1. Quantify material flammability under microgravity and partial gravity conditions.
        2. Identify critical fire hazards in human spaceflight habitats (Artemis Lunar Base & Mars Transit).
        3. Provide actionable fire prevention and suppression parameters for space mission architects.
        """)

        st.markdown("### Data Provenance")
        st.markdown("""
        - **NASA Technical Reports Server (NTRS):** Peer-reviewed flight reports, symposium presentations, and NASA standards (NASA-STD-6001).
        - **NASA Physical Sciences Informatics (PSI):** Quantitative flight data from ACME BRE, BASS-II, and SAFFIRE-I, -II, and -III missions.
        """)

        st.markdown("### How the App Works")
        a1, a2, a3 = st.columns(3)
        with a1:
            st.markdown("""
            <div class="step-card">
                <div style="font-size: 26px; font-weight: 800; color: #FF6A00; margin-bottom: 6px;">Database</div>
                <div style="font-weight: 700; margin-bottom: 4px;">SQLite (`data/flame.db`)</div>
                <div style="font-size: 13px; color: #94A3B8;">Stores cleaned normalized tables for 22 scanned files, 166 experiment records, and 12 PDF papers.</div>
            </div>
            """, unsafe_allow_html=True)
        with a2:
            st.markdown("""
            <div class="step-card">
                <div style="font-size: 26px; font-weight: 800; color: #FF6A00; margin-bottom: 6px;">Backend</div>
                <div style="font-weight: 700; margin-bottom: 4px;">FastAPI (`main.py`)</div>
                <div style="font-size: 13px; color: #94A3B8;">Serves parameterized REST endpoints with dynamic column pruning and float array parsing for oxygen.</div>
            </div>
            """, unsafe_allow_html=True)
        with a3:
            st.markdown("""
            <div class="step-card">
                <div style="font-size: 26px; font-weight: 800; color: #FF6A00; margin-bottom: 6px;">Frontend</div>
                <div style="font-weight: 700; margin-bottom: 4px;">Streamlit (`app.py`)</div>
                <div style="font-size: 13px; color: #94A3B8;">Interactive dashboard with NASA color palette, sticky top navigation, Plotly charts, and What-If simulator.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Project Team")
        st.markdown("""
        <div class="info-card">
            Developed as an aerospace fire safety platform delivering <i>“SI-Powered Fire Safety Insights from Microgravity Combustion Data.”</i>
        </div>
        """, unsafe_allow_html=True)
st.markdown("""
<div style="border-top: 1px solid #24344D; padding: 24px 0; margin-top: 48px; background-color: #0E1A2B; width: 100%;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; width: 100%;">
        <div>
            <div style="font-family: 'Space Grotesk', 'Segoe UI', Arial, sans-serif; font-size: 16px; font-weight: 700; color: #FF6A00; line-height: 1.2;">
                AeroFlame_Analytics
            </div>
            <div style="font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif; font-size: 13px; color: #94A3B8; line-height: 1.5; margin-top: 6px;">
                SI-Powered Fire Safety Insights from Microgravity Combustion Data
            </div>
        </div>
        <div style="font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif; font-size: 13px; color: #94A3B8; line-height: 1.7; text-align: right;">
            <div>NASA Technical Reports Server (NTRS)</div>
            <div>NASA Physical Sciences Informatics (PSI)</div>
        </div>
    </div>
    <div style="border-top: 1px solid rgba(36, 52, 77, 0.4); margin-top: 18px; padding-top: 14px; text-align: center; font-family: 'DM Sans', 'Segoe UI', Arial, sans-serif; font-size: 12px; color: #94A3B8;">
        Educational prototype. Risk levels are a simple rule, not a scientific model. • © 2026 AeroFlame_Analytics
    </div>
</div>
""", unsafe_allow_html=True)
