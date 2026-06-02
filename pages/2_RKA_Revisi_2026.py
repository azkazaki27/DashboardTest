import streamlit as st

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="RKA Revisi 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# LOAD CSS
# =====================================

from utils.style import load_css

load_css()

# IMPORT DATA
from utils.load_data_rka import (
    load_data,
    sheet_mapping
)

# TITLE

st.title("RKA Revisi 2026")

# MENU PILIH DATA

selected_menu = st.pills(
    "Pilih Data",
    list(sheet_mapping.keys()),
    default=None
)

# JUDUL
if selected_menu:

    st.markdown(
        f"""
        <h3 style='
            color:#00529C;
            margin-top:6px;
            margin-bottom:14px;
            font-weight:700;
            font-size:18px;
        '>
            Data {selected_menu}
        </h3>
        """,
        unsafe_allow_html=True
    )

# LOAD DATA
if selected_menu:

    try:

        df_clean = load_data(selected_menu)

        if df_clean.empty:

            st.warning(
                f"Data {selected_menu} belum tersedia."
            )

        else:

            # HTML TABLE
            styled_html = df_clean.to_html(
                index=False,
                classes="custom-table"
            )

            
            st.markdown(
                styled_html,
                unsafe_allow_html=True
            )

            st.dataframe(
                df_clean,
                height=600, # Mengunci tinggi tabel (muncul scroll vertikal)
                use_container_width=True, # Mengunci lebar (muncul scroll horizontal)
                hide_index=True
            )

    except Exception as e:

        st.warning(
            f"Data {selected_menu} gagal ditampilkan."
        )

        st.text(str(e))
