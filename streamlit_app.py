import streamlit as st
import base64

pg = st.navigation([
    st.Page("pages/1_Alma_Fact.py", title="Alma Fact"),
    st.Page("pages/2_RKA_Revisi_2026.py", title="RKA Revisi 2026"),
    st.Page("pages/3_Monitoring_Keragaan.py", title="Monitoring Keragaan"),
])
pg.run()

with open("assets/bri_logo_white.png", "rb") as f:
    data = base64.b64encode(f.read()).decode()

# 3. Tampilkan logo dengan pembungkus class khusus
st.sidebar.markdown(
    f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{data}" style="width: 1000px; margin-bottom: 0px;">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        /* Mengubah sidebar menjadi sistem Flexbox */
        [data-testid="stSidebarContent"] {
            display: flex;
            flex-direction: column;
        }
        
        /* Memaksa logo naik ke urutan pertama */
        [data-testid="stSidebarContent"] > div:has(.logo-container) {
            order: -1; 
            margin-bottom: 0px; 
            left-margin: 200px !important;
        }

        /* 1. Sembunyikan garis penarik visualnya */
        [data-testid="stSidebarResizeHandle"] {
            display: none !important;
        }

        /* 2. Kunci lebar sidebar HANYA ketika sidebar dalam keadaan TERBUKA */
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 200px !important;
            max-width: 200px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)