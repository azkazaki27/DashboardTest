import streamlit as st
from utils.style import load_css
import requests
import base64

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

# Memuat CSS eksternal milik Anda
try:
    load_css()
except:
    pass # Mengabaikan jika file utils/style.py sedang tidak bisa dimuat

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
# API & GOOGLE DRIVE
# =====================================

URL_API_GAS = (
    "https://script.google.com/macros/s/"
    "AKfycbzCrOOonKKyOUYMKF7sutUkA1nBkTNfZ7S09uuS_yk0cU_dqqo_2_nqLbtYD4h0AVrhyw/exec"
)

ID_FOLDER_UTAMA = "15nq6jbd0K56BEKsLlQqCtIi-y-GuQHHO"


# =====================================
# FUNGSI: LOAD FOLDER BULAN
# =====================================

@st.cache_data(ttl=600)
def ambil_daftar_bulan_otomatis(parent_id):
    url = f"{URL_API_GAS}?mode=getFolders&folderId={parent_id}"
    try:
        respon = requests.get(url)
        if respon.status_code == 200:
            data = respon.json()
            if "error" not in data:
                return {item['nama']: item['id'] for item in data}
    except:
        pass
    return {}


# =====================================
# FUNGSI: LOAD GAMBAR
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
                    # Trik thumbnail Google Drive dengan resolusi tinggi (w1600)
                    direct_url = f"https://drive.google.com/thumbnail?id={item['id']}&sz=w1600"
                    
                    daftar_link_gambar.append({
                        "nama": item['nama'],
                        "url": direct_url,
                        "id": item['id']
                    })
    except:
        pass
        
    return daftar_link_gambar


# =====================================
# FUNGSI: CUSTOM IMAGE VIEWER (MOBILE)
# =====================================

def render_image_viewer(url_gambar, tinggi=400):
    # Menyuntikkan HTML & JS Library Viewer.js ditambah fitur API Fullscreen bawaan Browser
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, user-scalable=yes">
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.3/viewer.min.css">
      <script src="https://cdnjs.cloudflare.com/ajax/libs/viewerjs/1.11.3/viewer.min.js"></script>
      <style>
        body {{ 
            margin: 0; display: flex; justify-content: center; align-items: center; 
            background: transparent; height: 100vh; overflow: hidden; 
        }}
        img {{ 
            max-width: 100%; max-height: {tinggi}px; cursor: zoom-in; 
            border-radius: 14px; border: 1px solid #E5E7EB; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.04); 
        }}
        /* Membuat latar belakang viewer menjadi hitam pekat saat fullscreen */
        .viewer-backdrop {{
            background-color: rgba(0, 0, 0, 1) !important;
        }}
      </style>
    </head>
    <body>
      <img id="image" src="{url_gambar}" alt="Laporan">
      <script>
        const img = document.getElementById('image');
        
        const viewer = new Viewer(img, {{
          inline: false,
          button: true,
          navbar: false,
          title: false,
          toolbar: {{ zoomIn: 1, zoomOut: 1, oneToOne: 1, reset: 1, play: 0 }},
          movable: true,
          zoomable: true,
          rotatable: false,
          scalable: false,
          transition: true
        }});

        // Fungsi untuk memaksa Iframe menerobos masuk ke mode Fullscreen HP
        function requestFullScreen() {{
          const doc = window.document.documentElement;
          const req = doc.requestFullscreen || doc.webkitRequestFullscreen || doc.mozRequestFullScreen || doc.msRequestFullscreen;
          if (req) {{
            req.call(doc);
          }}
        }}

        // Fungsi untuk mengembalikan ukuran ke semula saat ditutup
        function exitFullScreen() {{
          const doc = window.document;
          const exit = doc.exitFullscreen || doc.webkitExitFullscreen || doc.mozCancelFullScreen || doc.msExitFullscreen;
          if (exit) {{
            exit.call(doc);
          }}
        }}

        // Saat gambar diketuk & viewer mulai terbuka -> Masuk Fullscreen
        img.addEventListener('show', function () {{
          requestFullScreen();
        }});

        // Saat tombol X diketuk & viewer tertutup -> Keluar Fullscreen
        img.addEventListener('hidden', function () {{
          exitFullScreen();
        }});
      </script>
    </body>
    </html>
    """
    
    # Render menggunakan base64 agar aman dari blokir iframe
    b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    iframe_html = f'''
    <iframe src="data:text/html;base64,{b64}" 
            width="100%" 
            height="{tinggi + 20}" 
            style="border:none;" 
            allow="fullscreen" 
            allowfullscreen="true" 
            webkitallowfullscreen="true" 
            mozallowfullscreen="true">
    </iframe>
    '''
    st.markdown(iframe_html, unsafe_allow_html=True)


# =====================================
# KAMUS KANTOR
# =====================================

KAMUS_KANTOR = {
    "Kantor Cabang": ["KC Only"],
    "KCP Bintaro": ["KCP Bintaro"],
    "KCP BTC": ["KCP BTC"],
    "KCP Graha": ["KCP Graha"],
    "Konsol": ["Konsolidasi"]
}

# =====================================
# HEADER
# =====================================

st.markdown("""
<div class="dashboard-title">
    ALMA FACT
</div>
""", unsafe_allow_html=True)


# =====================================
# LOAD BULAN DARI DRIVE
# =====================================

with st.spinner("Sinkronisasi folder dari Google Drive..."):
    dict_bulan = ambil_daftar_bulan_otomatis(ID_FOLDER_UTAMA)

# =====================================
# VALIDASI & FILTER AREA
# =====================================

if not dict_bulan:
    st.error("Gagal memuat struktur folder Google Drive. Pastikan akses publik aktif.")
else:
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

    with st.spinner(f"Memuat laporan {pilihan_kantor}..."):
        semua_gambar = ambil_gambar_via_gas(id_folder_bulan)

    # =====================================
    # FILTER GAMBAR
    # =====================================
    gambar_terfilter = [
        g for g in semua_gambar
        if any(keyword.lower() in g['nama'].lower() for keyword in kata_kunci_list)
    ]

    # =====================================
    # HASIL & RENDER
    # =====================================
    if not gambar_terfilter:
        st.info(f"Tidak ada laporan {pilihan_kantor} di bulan {pilihan_bulan}.")
    else:
        st.markdown(f"""
        <div class="success-box">
            ✅ Berhasil memuat laporan {pilihan_kantor}
        </div>
        """, unsafe_allow_html=True)

        # =====================================
        # LOOP GAMBAR
        # =====================================
        for index, gbr in enumerate(gambar_terfilter, start=1):
            
            # Judul Laporan
            st.markdown(f"<div class='image-title'>📄 {gbr['nama']}</div>", unsafe_allow_html=True)

            # Memanggil fungsi Viewer kustom
            render_image_viewer(gbr['url'], tinggi=400)
            
            # Petunjuk untuk user mobile
            st.caption("💡 *Sentuh/Klik gambar untuk memperbesar (Zoom & Fullscreen)*")
            
            st.divider()
