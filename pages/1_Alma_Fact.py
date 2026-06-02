import streamlit as st
from utils.style import load_css
import requests

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="ALMA FACT",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# LOAD CSS
# =====================================

load_css()

st.markdown("""
<style>

/* Selectbox */
div[data-baseweb="select"] > div {
    min-height: 40px !important;
}

/* Button */
div.stButton > button {
    height: 40px !important;
    margin-top: 0px !important;
    font-size: 13px !important;
}

/* Dashboard Title */
.dashboard-title {
    color: #00529C !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    margin-bottom: 0px !important;
}

/* Image Title */
.image-title {
    color: #00529C;
    margin-top: 18px;
    margin-bottom: 6px;
    font-weight: 700;
    font-size: 15px;
}

/* Image Container */
.stImage img {
    border-radius: 14px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Success Box */
.success-box {
    background: #DCFCE7;
    color: #166534;
    padding: 12px 14px;
    border-radius: 10px;
    border: 1px solid #BBF7D0;
    margin-top: 14px;
    margin-bottom: 18px;
    font-weight: 600;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

import base64

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

/* =====================================
PRIMARY BUTTON
===================================== */

div.stButton > button:first-child {

    background-color: #22C55E !important;

    color: white !important;

    border: 1px solid #22C55E !important;

    border-radius: 10px !important;

    font-weight: 700 !important;

    height: 40px !important;

    font-size: 13px !important;

    transition: 0.2s ease;
}

div.stButton > button:first-child:hover {

    background-color: #16A34A !important;

    border-color: #16A34A !important;

    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================

st.markdown("""
<div style="color:#00529C; font-size:26px; font-weight:800; margin-bottom:0px;">
    ALMA FACT
</div>
""", unsafe_allow_html=True)

# =====================================
# API & GOOGLE DRIVE
# =====================================

URL_API_GAS = (
    "https://script.google.com/macros/s/"
    "AKfycbzCrOOonKKyOUYMKF7sutUkA1nBkTNfZ7S09uuS_yk0cU_dqqo_2_nqLbtYD4h0AVrhyw/exec"
)

ID_FOLDER_UTAMA = "15nq6jbd0K56BEKsLlQqCtIi-y-GuQHHO"

# =====================================
# LOAD FOLDER BULAN
# =====================================

@st.cache_data(ttl=600)
def ambil_daftar_bulan_otomatis(parent_id):

    url = f"{URL_API_GAS}?mode=getFolders&folderId={parent_id}"

    try:

        respon = requests.get(url)

        if respon.status_code == 200:

            data = respon.json()

            if "error" not in data:

                return {
                    item['nama']: item['id']
                    for item in data
                }

    except:
        pass

    return {}

# =====================================
# LOAD GAMBAR
# =====================================

@st.cache_data(ttl=600)
def ambil_gambar_via_gas(folder_id):

    daftar_link_gambar = []

    url = f"{URL_API_GAS}?mode=getImages&folderId={folder_id}"

    try:

        respon = requests.get(url)

        if respon.status_code == 200:

            data = respon.json()

            if "error" not in data:

                for item in data:

                    direct_url = (
                        f"https://drive.google.com/"
                        f"thumbnail?id={item['id']}&sz=w1600"
                    )

                    daftar_link_gambar.append({
                        "nama": item['nama'],
                        "url": direct_url
                    })

    except:
        pass

    return daftar_link_gambar

# =====================================
# KAMUS KANTOR
# =====================================

KAMUS_KANTOR = {
    "Kantor Cabang": [
        "KC Only"
    ],

    "KCP Bintaro": [
        "KCP Bintaro"
    ],

    "KCP BTC": [
        "KCP BTC"
    ],

    "KCP Graha": [
        "KCP Graha"
    ],

    "Konsol": [
        "Konsolidasi"
    ]
}

# =====================================
# LOAD BULAN
# =====================================

with st.spinner("Sinkronisasi folder dari Google Drive..."):

    dict_bulan = ambil_daftar_bulan_otomatis(
        ID_FOLDER_UTAMA
    )

# =====================================
# VALIDASI
# =====================================

if not dict_bulan:

    st.error(
        "Gagal memuat struktur folder Google Drive."
    )

else:

    # =====================================
    # FILTER AREA
    # =====================================

    col1, col2, col3 = st.columns([1,1,1])

    with col1:

        pilihan_bulan = st.selectbox(
            "Pilih Bulan",
            list(dict_bulan.keys()),
            label_visibility="collapsed"
        )

    with col2:

        pilihan_kantor = st.selectbox(
            "Pilih Kantor",
            list(KAMUS_KANTOR.keys()),
            label_visibility="collapsed"
        )

    with col3:

        tampilkan = st.button(
            "Tampilkan Data",
            use_container_width=True,
            type="primary"
        )

# =====================================
# TAMPILKAN DATA
# =====================================

if tampilkan:

    id_folder_bulan = dict_bulan[pilihan_bulan]

    kata_kunci_list = KAMUS_KANTOR[pilihan_kantor]

    with st.spinner(
        f"Memuat laporan {pilihan_kantor}..."
    ):

        semua_gambar = ambil_gambar_via_gas(
            id_folder_bulan
        )

    # =====================================
    # FILTER GAMBAR
    # =====================================

    gambar_terfilter = [

        g for g in semua_gambar

        if any(
            keyword.lower() in g['nama'].lower()
            for keyword in kata_kunci_list
        )
    ]

    # =====================================
    # VALIDASI
    # =====================================

    if not gambar_terfilter:

        st.info(
            f"Tidak ada laporan "
            f"{pilihan_kantor} "
            f"di bulan {pilihan_bulan}."
        )

    else:

        st.markdown(f"""
        <div class="success-box">
            ✅ Berhasil memuat laporan
            {pilihan_kantor}
        </div>
        """, unsafe_allow_html=True)

        # =====================================
        # LOOP GAMBAR
        # =====================================

        for index, gbr in enumerate(
            gambar_terfilter,
            start=1
        ):

            st.caption(gbr['nama'])

            st.image(
                gbr['url'],
                use_container_width=True
            )
