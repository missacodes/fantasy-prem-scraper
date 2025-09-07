import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, ColumnsAutoSizeMode
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="FPL Player Rankings", layout="wide")

st.markdown(
    """
    <style>
    h1 { font-size: 2.4rem !important; }
    .ag-theme-streamlit .ag-header-cell-label { font-size: 1rem; }
    .ag-theme-streamlit .ag-cell { font-size: 1rem; line-height: 1.9rem; }
    .ag-theme-streamlit .ag-header { min-height: 42px; }
    [data-testid="stAppViewContainer"] > .main {padding-left: 0rem; padding-right: 0rem;}
    .block-container {padding: 0.5rem 1rem 1.25rem 1rem; max-width: 100%;}
    </style>
    """, unsafe_allow_html=True
)

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

@st.cache_data(ttl=300)
def load_fpl():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    data = requests.get(url, timeout=30).json()
    players = pd.DataFrame(data["elements"])
    teams = pd.DataFrame(data["teams"])[["id", "name"]]
    team_map = dict(zip(teams["id"], teams["name"]))
    position_map = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}

    df = pd.DataFrame({
        "Name": players["first_name"] + " " + players["second_name"],
        "Club": players["team"].map(team_map),
        "Position": players["element_type"].map(position_map),
        "Price (£m)": players["now_cost"] / 10.0,
        "Total Points": players["total_points"],
        "Minutes": players["minutes"],
    })
    return df

st.title("⚽ FPL Player Rankings")

with st.sidebar:
    st.subheader("Data Refresh")
    auto = st.checkbox("Auto-refresh", value=True, help="Reload data on a timer.")
    minutes = st.slider("Every (minutes)", 1, 15, 5, 1)
    if auto:
        st_autorefresh(interval=minutes * 60 * 1000, key="auto-refresh")
    if st.button("Refresh now"):
        st.cache_data.clear()
        safe_rerun()

df = load_fpl()

left, main, right = st.columns([1, 6, 1])

with main:
    price_min = float(df["Price (£m)"].min())
    price_max = float(df["Price (£m)"].max())
    price_range = st.slider("Price (£m)", min_value=price_min, max_value=price_max,
                            value=(price_min, price_max), step=0.1)

    df = df[(df["Price (£m)"] >= price_range[0]) & (df["Price (£m)"] <= price_range[1])]
    df = df.sort_values("Total Points", ascending=False).reset_index(drop=True)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, sortable=True, filter=True, floatingFilter=True)
    gb.configure_column("Club", filter="agSetColumnFilter", filterParams={"suppressMiniFilter": False})
    gb.configure_column("Position", filter="agSetColumnFilter", filterParams={"suppressMiniFilter": False})
    gb.configure_column("Price (£m)", type=["numericColumn", "rightAligned"],
                        filter="agNumberColumnFilter", valueFormatter="x.toFixed(1)")
    gb.configure_pagination(enabled=False)  
    gb.configure_side_bar()                 
    gb.configure_grid_options(domLayout="normal", suppressMenuHide=False)
    go = gb.build()

    AgGrid(
        df,
        gridOptions=go,
        update_mode=GridUpdateMode.NO_UPDATE,
        fit_columns_on_grid_load=False,                    
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        theme="streamlit",
        height=720,
        enable_enterprise_modules=True,
    )
