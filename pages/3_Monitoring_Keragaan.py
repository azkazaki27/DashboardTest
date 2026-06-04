import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Monitoring Keragaan",
    layout="wide"
)
# CUSTOM CSS UNTUK ST.EXPANDER
st.markdown("""
<style>
/* 1. Warna header expander dalam kondisi normal (tertutup) */
[data-testid="stExpander"] details summary {
    background-color: #F8F9FA !important; /* Abu-abu sangat terang */
    color: #111827 !important; /* Teks hitam/gelap */
    border-radius: 8px !important;
    border: 1px solid #E5E7EB !important;
}

/* 2. Warna header ketika kursor diarahkan (hover) */
[data-testid="stExpander"] details summary:hover {
    background-color: #E5E7EB !important; 
}

/* 3. Warna header saat expander DIBUKA (menghilangkan warna hitam) */
[data-testid="stExpander"] details[open] summary {
    background-color: #EFF6FF !important; /* Warna biru sangat muda agar elegan */
    color: #00529C !important; /* Teks biru khas BRI */
    border-bottom: none !important;
    border-radius: 8px 8px 0 0 !important;
}

/* 4. Warna background area konten di dalam expander */
[data-testid="stExpander"] details[open] > div {
    background-color: #FFFFFF !important; /* Latar putih bersih */
    border-left: 1px solid #E5E7EB !important;
    border-right: 1px solid #E5E7EB !important;
    border-bottom: 1px solid #E5E7EB !important;
    border-radius: 0 0 8px 8px !important;
    padding: 16px !important;
}

/* Menghilangkan outline biru/hitam bawaan browser saat diklik */
[data-testid="stExpander"] details summary:focus {
    outline: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

from utils.style import load_css
load_css()


from utils.load_data import (
    load_data,
    sheet_mapping
)

# TITLE
st.title("Monitoring Keragaan")

# KPI WARNING FUNCTION
def status_kpi(x):

    if pd.isna(x):
        return "Merah"

    if x >= 99.99:
        return "Hijau"

    elif x >= 95:
        return "Kuning"

    else:
        return "Merah"


def get_kpi_df(df_clean, pencapaian_col):

    temp = df_clean.copy()

    temp["PENCAPAIAN_NUM"] = (
        temp[pencapaian_col]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    temp["PENCAPAIAN_NUM"] = pd.to_numeric(
        temp["PENCAPAIAN_NUM"],
        errors="coerce"
    )

    data = []

    current_kelompok = None

    for _, row in temp.iterrows():

        nama = str(
            row["MATA ANGGARAN"]
        ).upper().strip()

        sub1 = ""

        if "_1" in temp.columns:
            sub1 = str(
                row["_1"]
            ).upper().strip()

        # HEADER
        if "TOTAL PINJAMAN" in nama:

            current_kelompok = "TOTAL PINJAMAN"

        elif "TOTAL SML" in nama:

            current_kelompok = "TOTAL SML"

        elif "TOTAL NPL" in nama:

            current_kelompok = "TOTAL NPL"

        elif "TOTAL DPK" in nama:

            current_kelompok = "TOTAL DPK"
                # DETAIL DPK
        elif current_kelompok == "TOTAL DPK":

            sub2 = ""

            if "_2" in temp.columns:

                sub2 = str(
                    row["_2"]
                ).upper().strip()

            if "TABUNGAN" in sub2:

                data.append(
                    (
                        "TOTAL DPK",
                        "Tabungan",
                        row["PENCAPAIAN_NUM"]
                    )
                )

            elif "GIRO" in sub2:

                data.append(
                    (
                        "TOTAL DPK",
                        "Giro",
                        row["PENCAPAIAN_NUM"]
                    )
                )

            elif "DEPOSITO" in sub2:

                data.append(
                    (
                        "TOTAL DPK",
                        "Deposito",
                        row["PENCAPAIAN_NUM"]
                    )
                )

        # PINJAMAN / SML / NPL
        elif nama.startswith("A"):

            data.append(
                (
                    current_kelompok,
                    "Small",
                    row["PENCAPAIAN_NUM"]
                )
            )

        elif nama.startswith("B"):

            data.append(
                (
                    current_kelompok,
                    "Konsumer",
                    row["PENCAPAIAN_NUM"]
                )
            )

        elif nama.startswith("C"):

            data.append(
                (
                    current_kelompok,
                    "Micro",
                    row["PENCAPAIAN_NUM"]
                )
            )
    

    return pd.DataFrame(
        data,
        columns=[
            "Kelompok",
            "Segmen",
            "Pencapaian"
        ]
    )

# PILIH KANTOR
selected_kantor = st.pills(
    "Pilih Kantor",
    list(sheet_mapping.keys())
)

# LOAD DATA
if selected_kantor:

    df_clean, sheet_date = load_data(
        selected_kantor
    )

    def get_data_date_from_column(df):
        if "_6" not in df.columns:
            return None

        non_null_values = (
            df["_6"]
            .astype(str)
            .str.strip()
            .replace(["", "nan"], pd.NA)
            .dropna()
        )
        if non_null_values.empty:
            return None

        raw_value = non_null_values.iloc[0]
        for fmt in [
        ]:
            try:
                return datetime.strptime(raw_value, fmt).date()
            except Exception:
                continue

        return raw_value

    data_date = get_data_date_from_column(df_clean)

    if data_date is not None:
        st.subheader(f"Data {selected_kantor} - {data_date}")
    else:
        st.subheader(f"Data {selected_kantor}")

    # DATAFRAME
    today = sheet_date or pd.Timestamp.now()
    bulan_angka = today.month  # Menghasilkan angka 1-12
    tahun_ini = today.year

    bulan_indo = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    
    # Ambil nama bulan dan jadikan huruf besar semua (uppercase) untuk judul kolom
    nama_bulan_ini = bulan_indo[bulan_angka].upper()

    def find_dynamic_col(df, prefix, month_label):
        def parse_month_year(value):
            if value is None:
                return None

            raw = str(value).strip()
            if not raw:
                return None

            months = {
                "JANUARI": "01", "JAN": "01", "JANUARY": "01",
                "FEBRUARI": "02", "FEB": "02", "FEBRUARY": "02",
                "MARET": "03", "MAR": "03", "MARCH": "03",
                "APRIL": "04", "APR": "04",
                "MEI": "05", "MAY": "05",
                "JUNI": "06", "JUN": "06", "JUNE": "06",
                "JULI": "07", "JUL": "07", "JULY": "07",
                "AGUSTUS": "08", "AUG": "08", "AGU": "08", "AUGUST": "08",
                "SEPTEMBER": "09", "SEP": "09", "SEPT": "09",
                "OKTOBER": "10", "OKT": "10", "OCT": "10", "OCTOBER": "10",
                "NOVEMBER": "11", "NOV": "11",
                "DESEMBER": "12", "DES": "12", "DEC": "12", "DECEMBER": "12"
            }

            parts = raw.replace(".", "").split()
            if len(parts) >= 2 and parts[-1].isdigit():
                year = parts[-1]
                month = parts[-2].upper()
                if month in months:
                    return f"{year}-{months[month]}"

            return None

        target_norm = parse_month_year(month_label)
        row0 = df.iloc[0].fillna("").astype(str)

        # First choose direct prefix matches like RKA, GAP RKA, or PENCAPAIAN RKA
        candidates = [
            col for col in df.columns
            if col == prefix or col.startswith(prefix + "_")
        ]

        def column_matches_target(col):
            raw_label = row0.get(col, "").strip()
            norm = parse_month_year(raw_label)
            if norm and target_norm:
                return norm == target_norm
            return raw_label == month_label

        matching = [col for col in candidates if column_matches_target(col)]
        if matching:
            return matching[-1]

        # If RKA direct columns do not contain the current month,
        # fallback to the generic underscore columns.
        if prefix == "RKA":
            underscore_candidates = [
                col for col in df.columns
                if str(col).startswith("_")
            ]
            matching_underscore = [
                col for col in underscore_candidates
                if column_matches_target(col)
            ]
            if matching_underscore:
                return matching_underscore[-1]

        # Fallback by last available candidate
        if candidates:
            return candidates[-1]

        return None

    target_month_label = f"{bulan_indo[bulan_angka]} {tahun_ini}"

    kolom_asli_rka = find_dynamic_col(df_clean, "RKA", target_month_label)
    kolom_asli_gap = find_dynamic_col(df_clean, "GAP RKA", target_month_label)
    kolom_asli_pencapaian = find_dynamic_col(df_clean, "PENCAPAIAN RKA", target_month_label)
    
    # WARNING KPI
    merah = pd.DataFrame()
    kuning = pd.DataFrame()
    hijau = pd.DataFrame()

    try:

        kpi_df = get_kpi_df(
            df_clean,
            kolom_asli_pencapaian
        )

        kpi_df = (
            kpi_df
            .dropna(subset=["Pencapaian"])
            .drop_duplicates(
                subset=["Kelompok", "Segmen"],
                keep="first"
            )
        )
        allowed = [

                ("TOTAL PINJAMAN", "Small"),
                ("TOTAL PINJAMAN", "Konsumer"),
                ("TOTAL PINJAMAN", "Micro"),

                ("TOTAL SML", "Small"),
                ("TOTAL SML", "Konsumer"),
                ("TOTAL SML", "Micro"),

                ("TOTAL NPL", "Small"),
                ("TOTAL NPL", "Konsumer"),
                ("TOTAL NPL", "Micro"),

                ("TOTAL DPK", "Tabungan"),
                ("TOTAL DPK", "Giro"),
                ("TOTAL DPK", "Deposito")
            ]

        kpi_df = kpi_df[
            kpi_df.apply(
                lambda x:
                (x["Kelompok"], x["Segmen"])
                in allowed,
                axis=1
            )
        ].copy()

        kpi_df["Status"] = (
            kpi_df["Pencapaian"]
            .apply(status_kpi)
        )

        merah = kpi_df[
            kpi_df["Status"] == "Merah"
        ]

        kuning = kpi_df[
            kpi_df["Status"] == "Kuning"
        ]

        hijau = kpi_df[
            kpi_df["Status"] == "Hijau"
        ]

    except Exception as e:

        st.error(
            f"Gagal menampilkan KPI: {e}"
        )

    # DASHBOARD KPI
    col_warning, col_chart = st.columns([50, 50])

    # WARNING KPI (KIRI)
    with col_warning:

        c1, c2, c3 = st.columns(3)

        # MERAH
        with c1:

            html = ""

            for _, row in merah.iterrows():

                html += f"""
                <div style='margin-bottom:6px;font-size:13px;'>
                • {row['Kelompok']} {row['Segmen']}
                ({row['Pencapaian']:.2f}%)
                </div>
                """

            st.markdown(
                f"""
                <div style="
                    background:#FEE2E2;
                    padding:12px;
                    border-radius:10px;
                    border-left:5px solid #DC2626;
                    min-height:300px;
                    font-size:13px;
                    margin-bottom:12px;
                ">
                    <h4 style="color:#111827;font-size:14px;margin:0 0 8px 0;">
                        🔴 Perlu Perhatian ({len(merah)})
                    </h4>
                    {html}
                </div>
                """,
                unsafe_allow_html=True
            )

        # KUNING
        with c2:

            html = ""

            for _, row in kuning.iterrows():

                html += f"""
                <div style='margin-bottom:6px;font-size:13px;'>
                • {row['Kelompok']} {row['Segmen']}
                ({row['Pencapaian']:.2f}%)
                </div>
                """

            st.markdown(
                f"""
                <div style="
                    background:#FEF3C7;
                    padding:12px;
                    border-radius:10px;
                    border-left:5px solid #F59E0B;
                    min-height:300px;
                    font-size:13px;
                    margin-bottom:12px;
                ">
                    <h4 style="color:#111827;font-size:14px;margin:0 0 8px 0;">
                        🟡 Mendekati Target ({len(kuning)})
                    </h4>
                    {html}
                </div>
                """,
                unsafe_allow_html=True
            )

        # HIJAU
        with c3:

            html = ""

            for _, row in hijau.iterrows():

                html += f"""
                <div style='margin-bottom:6px;font-size:13px;'>
                • {row['Kelompok']} {row['Segmen']}
                ({row['Pencapaian']:.2f}%)
                </div>
                """

            st.markdown(
                f"""
                <div style="
                    background:#DCFCE7;
                    padding:12px;
                    border-radius:10px;
                    border-left:5px solid #16A34A;
                    min-height:300px;
                    font-size:13px;
                    margin-bottom:12px;
                ">
                    <h4 style="color:#111827;font-size:14px;margin:0 0 8px 0;">
                        🟢 Memenuhi Target ({len(hijau)})
                    </h4>
                    {html}
                </div>
                """,
                unsafe_allow_html=True
            )

    # GRAFIK KPI (KANAN)
    with col_chart:

        chart_df = kpi_df.copy()

        urutan_kelompok = [
            "TOTAL PINJAMAN",
            "TOTAL SML",
            "TOTAL NPL",
            "TOTAL DPK"
        ]

        urutan_segmen = [
            "Small",
            "Konsumer",
            "Micro",
            "Tabungan",
            "Giro",
            "Deposito"
        ]

        chart_df["Kelompok"] = pd.Categorical(
            chart_df["Kelompok"],
            categories=urutan_kelompok,
            ordered=True
        )

        chart_df["Segmen"] = pd.Categorical(
            chart_df["Segmen"],
            categories=urutan_segmen,
            ordered=True
        )

        chart_df = chart_df.sort_values(
            ["Kelompok", "Segmen"]
        )

        chart_df["Label"] = (
            chart_df["Kelompok"].astype(str)
            + "<br>"
            + chart_df["Segmen"].astype(str)
        )

        warna_bar = []

        for status in chart_df["Status"]:

            if status == "Merah":

                warna_bar.append("#DC2626")

            elif status == "Kuning":

                warna_bar.append("#F59E0B")

            else:

                warna_bar.append("#16A34A")

        fig = px.bar(
            chart_df,
            x="Label",
            y="Pencapaian",
            text="Pencapaian"
        )

        fig.update_traces(
            marker_color=warna_bar,
            texttemplate="%{text:.2f}%",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(
                color="white",
                size=10
            )
        )

        fig.update_layout(
            height=400,
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="",
            yaxis_title="Pencapaian (%)",
            showlegend=False,
            margin=dict(
                t=30,
                b=60,
                l=35,
                r=15
            ),
            font=dict(size=11),
            xaxis=dict(
                tickfont=dict(
                    color="black",
                    size=10
                )
            ),
            yaxis=dict(
                tickfont=dict(
                    color="black",
                    size=10
                ),
                range=[0, 110]
            )
        )

        fig.add_hline(
            y=95,
            line_dash="dash",
            line_color="#F59E0B",
            annotation_text="Target Kuning (95%)",
            annotation_position="top right",
            annotation_font=dict(
                color="black",
                size=10
            )
        )

        fig.add_hline(
            y=100,
            line_dash="dash",
            line_color="#16A34A",
            annotation_text="Target Hijau (99,99%)",
            annotation_position="top right",
            annotation_font=dict(
                color="black",
                size=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def get_total_row(df, keyword):
        keyword = keyword.upper()
        found = df[
            df["MATA ANGGARAN"].astype(str).str.upper().str.contains(keyword, na=False)
        ]
        return found.iloc[0] if not found.empty else None

    def get_row_metrics(row):
        if row is None:
            return ["", "", "","", "", "", "", ""]
        hari_ini = row.get("_6", "")
        ytd = row.get("DELTA", "")
        mtd = row.get("_7", "")
        dtd = row.get("_8", "")
        yoy = row.get("_9", "")
        rka = row.get(kolom_asli_rka, "") if kolom_asli_rka else ""
        gap = row.get(kolom_asli_gap, "") if kolom_asli_gap else ""
        pencapaian = row.get(kolom_asli_pencapaian, "") if kolom_asli_pencapaian else ""
        return [hari_ini, ytd, mtd, dtd, yoy, rka, gap, pencapaian]

    total_pinjaman_row = get_total_row(df_clean, "TOTAL PINJAMAN")
    total_sml_row = get_total_row(df_clean, "TOTAL SML")
    total_npl_row = get_total_row(df_clean, "TOTAL NPL")
    total_dpk_row = get_total_row(df_clean, "TOTAL DPK")

    def render_metrics(title, row):
        def format_pencapaian_box(value):
            text = str(value).strip()
            try:
                numeric = float(text.replace("%", "").replace(",", "."))
            except Exception:
                numeric = None

            if numeric is None:
                background = "#F3F4F6"
                color = "#111827"
            elif numeric < 95:
                background = "#FEE2E2"
                color = "#991B1B"
            elif numeric < 100:
                background = "#FEF3C7"
                color = "#92400E"
            else:
                background = "#DCFCE7"
                color = "#166534"

            return (
                f"<div style='display:inline-flex; align-items:center; justify-content:center;"
                f" min-height:28px; padding:3px 10px; border-radius:12px;"
                f" background:{background}; color:{color}; font-weight:700; font-size:18px; line-height:1.1;"
                f" vertical-align:middle;'>{text}</div>"
            )

        def format_value(value, label=None):
            text = str(value)
            if label == "PENCAPAIAN RKA":
                return format_pencapaian_box(text)
            if text.strip().startswith("-"):
                color = "#DC2626"
            else:
                color = "#00529C"
            return f"<div style='font-size:18px; font-weight:700; color:{color};'>{text}</div>"

        values = get_row_metrics(row)
        labels = ["HARI INI", "YTD", "MTD", "DTD", "YOY", "RKA", "GAP RKA", "PENCAPAIAN RKA"]
        
        #HTML UNTUK DESKTOP
        desktop_html = f"<div class='kpi-title-desktop kpi-title'>{title}</div><div class='kpi-desktop'>"
        for idx, label in enumerate(labels):
            val_html = format_value(values[idx], label)
            desktop_html += f"<div class='kpi-box'><div class='kpi-label'>{label}</div>{val_html}</div>"
        desktop_html += "</div>"

        #HTML UNTUK MOBILE (CARD STYLE)
        hari_ini_val = format_value(values[0], labels[0])
        penc_rka_val = format_value(values[7], labels[7])

        mobile_html = f"""
        <div class='kpi-mobile'>
            <div class='kpi-mobile-header'>
                <div class='kpi-mobile-title'>{title}</div>
            </div>
            <div class='kpi-mobile-main'>
                <div class='kpi-mobile-val-box'>
                    <div class='kpi-label'>{labels[0]}</div>
                    {hari_ini_val}
                </div>
                <div class='kpi-mobile-val-box right'>
                    <div class='kpi-label'>{labels[7]}</div>
                    {penc_rka_val}
                </div>
            </div>
            <details class='kpi-mobile-details'>
                <summary>Tampilkan Semua Metrik</summary>
                <div class='kpi-mobile-expanded'>
        """
        for idx in range(1, 7): # Menambahkan sisanya (YTD s.d. GAP RKA) ke dalam dropdown
            val_html = format_value(values[idx], labels[idx])
            mobile_html += f"<div class='kpi-box'><div class='kpi-label'>{labels[idx]}</div>{val_html}</div>"
            
        mobile_html += "</div></details></div>"

        #GABUNGAN CSS & RENDER
        css = """
        <style>
        .kpi-container { margin-bottom: 1.5rem; font-family: sans-serif; }
        .kpi-title { font-size: 1.25rem; font-weight: 700; color: #1F2937; margin-bottom: 12px; }
        .kpi-label { font-size: 10px; font-weight: 600; color: #6B7280; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.5px;}
        
        /* Desktop */
        .kpi-desktop { display: grid; grid-template-columns: repeat(8, 1fr); gap: 10px; align-items: center; margin-bottom: 10px; }
        .kpi-box { display: flex; flex-direction: column; }
        
        /* Mobile */
        .kpi-mobile { display: none; background: #ffffff; border-radius: 16px; padding: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); border: 1px solid #f3f4f6; margin-bottom: 15px;}
        .kpi-mobile-header { margin-bottom: 12px; border-bottom: 1px solid #f3f4f6; padding-bottom: 8px;}
        .kpi-mobile-title { font-size: 18px; font-weight: 700; color: #00529C; }
        .kpi-mobile-main { display: flex; justify-content: space-between; align-items: center; }
        .kpi-mobile-val-box { display: flex; flex-direction: column; gap: 4px; }
        .kpi-mobile-val-box.right { align-items: flex-end; }
        
        .kpi-mobile-details { margin-top: 16px; }
        .kpi-mobile-details summary { font-size: 12px; color: #3B82F6; cursor: pointer; list-style: none; text-align: center; background: #EFF6FF; padding: 8px; border-radius: 8px; font-weight: 600; transition: background 0.2s;}
        .kpi-mobile-details summary::-webkit-details-marker { display: none; }
        .kpi-mobile-details[open] summary { margin-bottom: 12px; background: #F3F4F6; color: #4B5563; }
        .kpi-mobile-expanded { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
        
        /* Logika Responsif */
        @media (max-width: 768px) {
            .kpi-desktop, .kpi-title-desktop { display: none !important; }
            .kpi-mobile { display: block !important; }
        }
        </style>
        """
        
        full_html = css + f"<div class='kpi-container'>{desktop_html}{mobile_html}</div>"
        st.markdown(full_html, unsafe_allow_html=True)

    def get_detail_rows(df, total_keyword):
        """Extract child rows between a total and the next total"""
        total_keyword = total_keyword.upper()
        total_idx = None
        next_total_idx = None
        
        # Find the total row
        for idx in range(len(df)):
            if total_keyword in str(df.iloc[idx]["MATA ANGGARAN"]).upper():
                total_idx = idx
                break
        
        if total_idx is None:
            return pd.DataFrame()
        
        # Find the next total; stop before the next summary block.
        for idx in range(total_idx + 1, len(df)):
            mata = str(df.iloc[idx]["MATA ANGGARAN"]).upper()
            if ("TOTAL" in mata) or "POSISI DPK" in mata:
                next_total_idx = idx
                break
        
        if next_total_idx is None:
            next_total_idx = len(df)
        
        # Extract rows between total and next total. Some DPK detail rows use the _2 column
        # for their item labels, so preserve those even when MATA ANGGARAN is blank.
        detail_df = df.iloc[total_idx + 1:next_total_idx].copy()
        if total_keyword == "TOTAL DPK" and "_2" in detail_df.columns:
            detail_df = detail_df[
                (detail_df["MATA ANGGARAN"].astype(str).str.strip() != "")
                | (detail_df["_2"].astype(str).str.strip() != "")
            ].reset_index(drop=True)
        else:
            detail_df = detail_df[
                detail_df["MATA ANGGARAN"].astype(str).str.strip() != ""
            ].reset_index(drop=True)
        return detail_df

    def get_item_label(mata_str):
        """Convert item names to readable labels"""
        mata_clean = str(mata_str).strip()
        
        # Simple mapping for common labels
        label_map = {
            "A.": "A. Small",
            "B.": "B. Consumer",
            "C.": "C. Micro",
            "RITEL": "Retail"
        }
        
        return label_map.get(mata_clean, mata_clean)

    def filter_detail_items_by_segment(detail_df, parent_total=None):
        """Hide unsupported item segments based on the selected sheet."""
        if detail_df.empty:
            return detail_df
            
        if parent_total is None:
            return detail_df

        parent_total = str(parent_total).upper().strip()
        
        # Special handling for TOTAL DPK - show only rows with item types in _2 column
        if parent_total == "TOTAL DPK":
            # Filter to show only rows where _2 column contains TABUNGAN, GIRO, or DEPOSITO
            if "_2" in detail_df.columns:
                mask = detail_df["_2"].astype(str).str.upper().str.strip().str.contains(r"TABUNGAN|GIRO|DEPOSITO", regex=True, na=False)
                return detail_df[mask].reset_index(drop=True)
            return detail_df.iloc[0:0]  # Return empty if _2 column doesn't exist
        
        if parent_total not in ["TOTAL PINJAMAN", "TOTAL SML", "TOTAL NPL"]:
            return detail_df

        allowed_segments = {
            "KCP BTC": {
                "TOTAL PINJAMAN": ["A.","B.", "C."],
                "TOTAL SML": ["A.","B.", "C."],
                "TOTAL NPL": ["A.","B.", "C."]
            },
            "KCP Bintaro": {
                "TOTAL PINJAMAN": ["A.","B.", "C."],
                "TOTAL SML": ["A.","B.", "C."],
                "TOTAL NPL": ["A.","B.", "C."]
            },
            "KCP Graha": {
                "TOTAL PINJAMAN": ["A.","B.", "C."],
                "TOTAL SML": ["A.","B.", "C."],
                "TOTAL NPL": ["A.","B.", "C."]
            }
        }

        if selected_kantor in ["Konsolidasi", "Kantor Cabang"]:
            return detail_df

        allowed = allowed_segments.get(selected_kantor, {}).get(parent_total)
        if not allowed:
            return detail_df

        mask = detail_df["MATA ANGGARAN"].astype(str).str.upper().str.strip().str.startswith(tuple(allowed))
        return detail_df[mask].reset_index(drop=True)

    def display_detail_items(detail_df, cols_to_show, parent_total=None):
        """Display detail items in aligned columns like metrics.
        parent_total: optional string like 'TOTAL DPK' to apply contextual labels
        """
        if detail_df.empty:
            return

        detail_df = filter_detail_items_by_segment(detail_df, parent_total)
        if detail_df.empty:
            return

        def format_pencapaian_box(value):
            text = str(value).strip()
            try:
                numeric = float(text.replace("%", "").replace(",", ".").strip())
            except Exception:
                numeric = None

            if numeric is None:
                background = "#F3F4F6"
                color = "#111827"
            elif numeric < 95:
                background = "#FEE2E2"
                color = "#991B1B"
            elif numeric < 100:
                background = "#FEF3C7"
                color = "#92400E"
            else:
                background = "#DCFCE7"
                color = "#166534"

            return (
                f"<span style='display:inline-flex; align-items:center; justify-content:center;"
                f" min-height:16px; padding:4px 8px; border-radius:12px;"
                f" background:{background}; color:{color}; font-weight:700;"
                f" font-size:14px; line-height:1.2; vertical-align:middle; text-align:right;'>"
                f"{text}</span>"
            )

        def format_value_color(value, label=None):
            text = str(value).strip()
            if label == "PENCAPAIAN RKA":
                return format_pencapaian_box(text)
            if text.startswith("-"):
                color = "#DC2626"
            else:
                color = "#00529C"
            return f"<span style='color:{color}; font-size:13px; font-weight:600;'>{text}</span>"

        # Map column names to display names
        col_mapping = {
            "DELTA": "YTD", "_6": "HARI INI", "_7": "MTD", "_8": "DTD", "_9": "YOY",
            kolom_asli_rka: "RKA", kolom_asli_gap: "GAP RKA", kolom_asli_pencapaian: "PENCAPAIAN RKA"
        }

        # Contextual label maps per parent total
        parent_label_map = {
            "TOTAL DPK": {
                "tabungan": "Tabungan", "TABUNGAN": "Tabungan",
                "giro": "Giro", "GIRO": "Giro",
                "deposito": "Deposito", "DEPOSITO": "Deposito"
            },
        }

        # Filter cols_to_show to only those that exist in dataframe
        available_cols = [c for c in cols_to_show if c in detail_df.columns]

        # Extract metric columns (skip MATA ANGGARAN)
        metric_cols = available_cols[1:]
        metric_labels = [col_mapping.get(c, c) for c in metric_cols]
        
        # Ekstrak index untuk metric utama di mobile
        hari_ini_idx = metric_cols.index("_6") if "_6" in metric_cols else -1
        pencapaian_idx = metric_cols.index(kolom_asli_pencapaian) if kolom_asli_pencapaian in metric_cols else -1

        html_str = "<div class='detail-container'>"

        #HTML UNTUK DESKTOP (Tabel Horizontal)
        html_str += "<div class='detail-desktop'>"
        
        # Header Row
        html_str += "<div class='detail-row header'>"
        html_str += "<div class='detail-item-name'>ITEM</div>"
        for label in metric_labels:
            html_str += f"<div class='detail-metric-header'>{label}</div>"
        html_str += "</div>"

        # Data Rows
        for idx, row in detail_df[available_cols].iterrows():
            raw_item = str(row.iloc[0]).strip()
            
            # For DPK, use _2 column value if available
            if parent_total == "TOTAL DPK" and "_2" in detail_df.columns:
                raw_item = str(detail_df.iloc[idx]["_2"]).strip()

            raw_item_lower = raw_item.lower().strip()

            # apply contextual mapping if exists
            if parent_total and parent_total in parent_label_map:
                item_name = parent_label_map[parent_total].get(raw_item_lower)
                if not item_name:
                    item_name = parent_label_map[parent_total].get(raw_item)
                if not item_name:
                    item_name = get_item_label(raw_item)
            else:
                item_name = get_item_label(raw_item)
            
            html_str += "<div class='detail-row'>"
            html_str += f"<div class='detail-item-name'>{item_name}</div>"
            for i, label in enumerate(metric_labels):
                html_str += f"<div class='detail-metric-val'>{format_value_color(row.iloc[i + 1], label)}</div>"
            html_str += "</div>"
            
        html_str += "</div>" 

        # --- HTML UNTUK MOBILE (Stacked Card) ---
        html_str += "<div class='detail-mobile'>"
        for idx, row in detail_df[available_cols].iterrows():
            raw_item = str(row.iloc[0]).strip()
            
            if parent_total == "TOTAL DPK" and "_2" in detail_df.columns:
                raw_item = str(detail_df.iloc[idx]["_2"]).strip()

            raw_item_lower = raw_item.lower().strip()
            
            if parent_total and parent_total in parent_label_map:
                item_name = parent_label_map[parent_total].get(raw_item_lower) or parent_label_map[parent_total].get(raw_item) or get_item_label(raw_item)
            else:
                item_name = get_item_label(raw_item)
            
            val_hari_ini = format_value_color(row.iloc[hari_ini_idx + 1], "HARI INI") if hari_ini_idx != -1 else "-"
            val_pencapaian = format_value_color(row.iloc[pencapaian_idx + 1], "PENCAPAIAN RKA") if pencapaian_idx != -1 else "-"

            html_str += f"""
            <div class='dmc-card'>
                <div class='dmc-header'>{item_name}</div>
                <div class='dmc-main'>
                    <div class='dmc-box'>
                        <div class='dmc-label'>HARI INI</div><div>{val_hari_ini}</div>
                    </div>
                    <div class='dmc-box' style='text-align:right;'>
                        <div class='dmc-label'>PENCAPAIAN</div><div>{val_pencapaian}</div>
                    </div>
                </div>
                <details class='dmc-details'>
                    <summary>Detail Lainnya</summary>
                    <div class='dmc-expanded'>
            """
            for i, label in enumerate(metric_labels):
                if label not in ["HARI INI", "PENCAPAIAN RKA"]:
                    html_str += f"<div class='dmc-box'><div class='dmc-label'>{label}</div><div>{format_value_color(row.iloc[i + 1], label)}</div></div>"
            html_str += "</div></details></div>"
        html_str += "</div></div>"

        #GABUNGAN CSS & RENDER
        css = """
        <style>
        /* CSS Desktop (Flexbox Horizontal) */
        .detail-desktop { display: flex; flex-direction: column; width: 100%; margin-top: 10px; }
        .detail-row { display: flex; flex-direction: row; align-items: center; justify-content: space-between; border-bottom: 1px solid #f3f4f6; padding: 10px 0; width: 100%; }
        .detail-row.header { border-bottom: 2px solid #e5e7eb; padding-bottom: 2px; margin-bottom: 4px; }
        
        .detail-item-name { flex: 2; min-width: 120px; font-size: 12px; font-weight: 700; color: #111827; }
        .detail-metric-header { flex: 1; text-align: right; font-size: 11px; font-weight: 7000; color: #4B5563; text-transform: uppercase; }
        .detail-metric-val { flex: 1; text-align: right; white-space: nowrap; }
        
        /* CSS Mobile */
        .detail-mobile { display: none; flex-direction: column; gap: 12px; margin-top: 10px;}
        .dmc-card { background: #fafafa; border: 1px solid #e5e7eb; border-radius: 12px; padding: 14px; }
        .dmc-header { font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 10px; border-bottom: 1px solid #eaeaea; padding-bottom: 8px;}
        .dmc-main { display: flex; justify-content: space-between; align-items: center; }
        .dmc-box { display: flex; flex-direction: column; gap: 4px;}
        .dmc-label { font-size: 10px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px;}
        
        .dmc-details { margin-top: 12px; }
        .dmc-details summary { font-size: 12px; color: #4B5563; cursor: pointer; text-align: center; background: #e5e7eb; padding: 6px; border-radius: 6px; font-weight: 600; list-style: none;}
        .dmc-details summary::-webkit-details-marker { display: none; }
        .dmc-expanded { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 12px; padding-top: 12px; border-top: 1px dashed #e5e7eb; }

        /* Logika Responsif */
        @media (max-width: 768px) {
            .detail-desktop { display: none !important; }
            .detail-mobile { display: flex !important; }
        }
        </style>
        """
        st.markdown(css + html_str, unsafe_allow_html=True)
        
    cols_to_display = ["MATA ANGGARAN", "_6", "DELTA", "_7", "_8", "_9"]
    if kolom_asli_rka and kolom_asli_rka in df_clean.columns:
        cols_to_display.append(kolom_asli_rka)
    if kolom_asli_gap and kolom_asli_gap in df_clean.columns:
        cols_to_display.append(kolom_asli_gap)
    if kolom_asli_pencapaian and kolom_asli_pencapaian in df_clean.columns:
        cols_to_display.append(kolom_asli_pencapaian)

    def to_number(x):

        try:

            return float(
                str(x)
                .replace(".", "")
                .replace(",", ".")
                .replace("%", "")
            )

        except:

            return 0


    def calc_growth(old_value, new_value):

        if old_value == 0:
            return 0

        return (
            (new_value - old_value)
            / abs(old_value)
        ) * 100

    header_row = df_clean.iloc[0].fillna("").astype(str)

    current_value = to_number(
    total_pinjaman_row["_6"]
    )

    yoy_base = to_number(
        total_pinjaman_row["POSISI"]
    )

    ytd_base = to_number(
        total_pinjaman_row["_3"]
    )

    mtd_base = to_number(
        total_pinjaman_row["_4"]
    )

    dtd_base = to_number(
        total_pinjaman_row["_5"]
    )

    yoy_growth = calc_growth(
        yoy_base,
        current_value
    )

    ytd_growth = calc_growth(
        ytd_base,
        current_value
    )

    mtd_growth = calc_growth(
        mtd_base,
        current_value
    )

    dtd_growth = calc_growth(
        dtd_base,
        current_value
    )

    label_yoy = str(header_row["POSISI"])
    label_ytd = str(header_row["_3"])
    label_mtd = str(header_row["_4"])
    label_dtd = str(header_row["_5"])
    label_current = str(header_row["_6"])

    # ANALISIS PERTUMBUHAN
    tab_yoy, tab_ytd, tab_mtd, tab_dtd = st.tabs(
        ["YOY", "YTD", "MTD", "DTD"]
    )

    with tab_yoy:

        yoy_compare = pd.DataFrame({

            "Kelompok": [
                "Pinjaman",
                "Pinjaman",
                "SML",
                "SML",
                "NPL",
                "NPL",
                "DPK",
                "DPK"
            ],

            "Periode": [
                label_yoy,
                label_current,
                label_yoy,
                label_current,
                label_yoy,
                label_current,
                label_yoy,
                label_current
            ],

            "Nilai": [

                to_number(total_pinjaman_row["POSISI"]),
                to_number(total_pinjaman_row["_6"]),

                to_number(total_sml_row["POSISI"]),
                to_number(total_sml_row["_6"]),

                to_number(total_npl_row["POSISI"]),
                to_number(total_npl_row["_6"]),

                to_number(total_dpk_row["POSISI"]),
                to_number(total_dpk_row["_6"])
            ]
        })

        fig_yoy = px.bar(
            yoy_compare,
            x="Kelompok",
            y="Nilai",
            color="Periode",
            barmode="group",
            text="Nilai",
            title=f"Perbandingan YOY ({label_yoy} & {label_current})"
        )

        max_value = yoy_compare["Nilai"].max()

        fig_yoy.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            textfont=dict(
                color="black",
                size=14
            )
        )

        fig_yoy.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_color="black",
            title_font=dict(
                color="black"
            ),
            xaxis=dict(
            title_font=dict(color="black"),
            tickfont=dict(color="black"),
            showgrid=False
            ),

            yaxis=dict(
                title_font=dict(color="black"),
                tickfont=dict(color="black"),
                range=[0, max_value * 1.20],
                showgrid=False
            ),

            legend=dict(
                title_font=dict(color="black"),
                font=dict(color="black")
            ),

            margin=dict(
                t=70
            ),
            height=450
        )

        st.plotly_chart(
            fig_yoy,
            use_container_width=True
        )

    with tab_ytd:

        ytd_compare = pd.DataFrame({

            "Kelompok": [
                "Pinjaman",
                "Pinjaman",
                "SML",
                "SML",
                "NPL",
                "NPL",
                "DPK",
                "DPK"
            ],

            "Periode": [
                label_ytd,
                label_current,
                label_ytd,
                label_current,
                label_ytd,
                label_current,
                label_ytd,
                label_current
            ],

            "Nilai": [

                to_number(total_pinjaman_row["_3"]),
                to_number(total_pinjaman_row["_6"]),

                to_number(total_sml_row["_3"]),
                to_number(total_sml_row["_6"]),

                to_number(total_npl_row["_3"]),
                to_number(total_npl_row["_6"]),

                to_number(total_dpk_row["_3"]),
                to_number(total_dpk_row["_6"])
            ]
        })

        fig_ytd = px.bar(
            ytd_compare,
            x="Kelompok",
            y="Nilai",
            color="Periode",
            barmode="group",
            text="Nilai",
            title=f"Perbandingan YTD ({label_ytd} & {label_current})"
        )

        max_value = ytd_compare["Nilai"].max()

        fig_ytd.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            textfont=dict(
                color="black",
                size=14
            )
        )

        fig_ytd.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_color="black",
            title_font=dict(
                color="black"
            ),
            xaxis=dict(
            title_font=dict(color="black"),
            tickfont=dict(color="black"),
            showgrid=False
            ),

            yaxis=dict(
                title_font=dict(color="black"),
                tickfont=dict(color="black"),
                range=[0, max_value * 1.20],
                showgrid=False
            ),

            legend=dict(
                title_font=dict(color="black"),
                font=dict(color="black")
            ),
            margin=dict(
                t=70
            ),
            height=450
        )

        st.plotly_chart(
            fig_ytd,
            use_container_width=True
        )

    with tab_mtd:

        mtd_compare = pd.DataFrame({

            "Kelompok": [
                "Pinjaman",
                "Pinjaman",
                "SML",
                "SML",
                "NPL",
                "NPL",
                "DPK",
                "DPK"
            ],

            "Periode": [
                label_mtd,
                label_current,
                label_mtd,
                label_current,
                label_mtd,
                label_current,
                label_mtd,
                label_current
            ],

            "Nilai": [

                to_number(total_pinjaman_row["_4"]),
                to_number(total_pinjaman_row["_6"]),

                to_number(total_sml_row["_4"]),
                to_number(total_sml_row["_6"]),

                to_number(total_npl_row["_4"]),
                to_number(total_npl_row["_6"]),

                to_number(total_dpk_row["_4"]),
                to_number(total_dpk_row["_6"])
            ]
        })

        fig_mtd = px.bar(
            mtd_compare,
            x="Kelompok",
            y="Nilai",
            color="Periode",
            barmode="group",
            text="Nilai",
            title=f"Perbandingan MTD ({label_mtd} & {label_current})"
        )

        max_value = mtd_compare["Nilai"].max()

        fig_mtd.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            textfont=dict(
                color="black",
                size=14
            )
        )

        fig_mtd.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_color="black",
            title_font=dict(
                color="black"
            ),
            xaxis=dict(
            title_font=dict(color="black"),
            tickfont=dict(color="black"),
            showgrid=False
            ),

            yaxis=dict(
                title_font=dict(color="black"),
                tickfont=dict(color="black"),
                range=[0, max_value * 1.20],
                showgrid=False
            ),

            legend=dict(
                title_font=dict(color="black"),
                font=dict(color="black")
            ),
            margin=dict(
                t=70
            ),
            height=450
        )

        st.plotly_chart(
            fig_mtd,
            use_container_width=True
        )

    with tab_dtd:

        dtd_compare = pd.DataFrame({

            "Kelompok": [
                "Pinjaman",
                "Pinjaman",
                "SML",
                "SML",
                "NPL",
                "NPL",
                "DPK",
                "DPK"
            ],

            "Periode": [
                label_dtd,
                label_current,
                label_dtd,
                label_current,
                label_dtd,
                label_current,
                label_dtd,
                label_current
            ],

            "Nilai": [

                to_number(total_pinjaman_row["_5"]),
                to_number(total_pinjaman_row["_6"]),

                to_number(total_sml_row["_5"]),
                to_number(total_sml_row["_6"]),

                to_number(total_npl_row["_5"]),
                to_number(total_npl_row["_6"]),

                to_number(total_dpk_row["_5"]),
                to_number(total_dpk_row["_6"])
            ]
        })

        fig_dtd = px.bar(
            dtd_compare,
            x="Kelompok",
            y="Nilai",
            color="Periode",
            barmode="group",
            text="Nilai",
            title=f"Perbandingan DTD ({label_dtd} & {label_current})"
        )

        max_value = dtd_compare["Nilai"].max()

        fig_dtd.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
            cliponaxis=False,
            textfont=dict(
                color="black",
                size=14
            )
        )

        fig_dtd.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font_color="black",
            title_font=dict(
                color="black"
            ),
            xaxis=dict(
            title_font=dict(color="black"),
            tickfont=dict(color="black"),
            showgrid=False
            ),

            yaxis=dict(
                title_font=dict(color="black"),
                tickfont=dict(color="black"),
                range=[0, max_value * 1.20],
                showgrid=False
            ),

            legend=dict(
                title_font=dict(color="black"),
                font=dict(color="black")
            ),
            margin=dict(
                t=70
            ),
            height=450
        )

        st.plotly_chart(
            fig_dtd,
            use_container_width=True
        )

    render_metrics("Total Pinjaman", total_pinjaman_row)
    pinjaman_details = get_detail_rows(df_clean, "TOTAL PINJAMAN")
    if not pinjaman_details.empty:
        with st.expander("Detail Items"):
            display_detail_items(pinjaman_details, cols_to_display, "TOTAL PINJAMAN")

    render_metrics("Total SML", total_sml_row)
    sml_details = get_detail_rows(df_clean, "TOTAL SML")
    if not sml_details.empty:
        with st.expander("Detail Items"):
            display_detail_items(sml_details, cols_to_display, "TOTAL SML")

    render_metrics("Total NPL", total_npl_row)
    npl_details = get_detail_rows(df_clean, "TOTAL NPL")
    if not npl_details.empty:
        with st.expander("Detail Items"):
            display_detail_items(npl_details, cols_to_display, "TOTAL NPL")

    render_metrics("Total DPK", total_dpk_row)
    dpk_details = get_detail_rows(df_clean, "TOTAL DPK")
    if not dpk_details.empty:
        with st.expander("Detail Items"):
            display_detail_items(dpk_details, cols_to_display, "TOTAL DPK")

    # 2. Tentukan nama kolom ALIAS (Nickname) yang ingin ditampilkan di UI
    alias_rka = f"RKA"
    alias_gap = f"GAP RKA"
    alias_pencapaian = f"PENCAPAIAN RKA"

    # 3. Buat dictionary untuk memetakan nama asli ke nama alias
    rename_mapping = {
        kolom_asli_rka: alias_rka,
        kolom_asli_gap: alias_gap,
        kolom_asli_pencapaian: alias_pencapaian
    }

    # FILTER & TAMPILKAN
    # Masukkan nama asli ke target kolom
    target_kolom_dinamis = [
        kolom_asli_rka,
        kolom_asli_gap,
        kolom_asli_pencapaian
    ]
    
    # KELUARKAN "_10", "GAP RKA_2", dll dari kolom wajib karena sekarang mereka dinamis
    kolom_wajib = ["NO.", "MATA ANGGARAN", "_1", "_2", "POSISI", "_3", "_4", "_5", "_6", "DELTA", "_7", "_8", "_9"]  

    # Validasi: Pastikan kolom dinamis yang dicari memang sudah ditarik dari sheet
    kolom_tersedia = [col for col in target_kolom_dinamis if col in df_clean.columns]
    kolom_final = kolom_wajib + kolom_tersedia

    # Buat salinan dataframe khusus untuk ditampilkan, lalu rename nama kolomnya
    df_tampil = df_clean[kolom_final].rename(columns=rename_mapping)

    rename_mapping = {
        # 1. Mapping kolom dinamis (dari kode sebelumnya)
        kolom_asli_rka: alias_rka,
        kolom_asli_gap: alias_gap,
        kolom_asli_pencapaian: alias_pencapaian,
        
        # 2. Trik Spasi Kosong: Ubah kolom-kolom realisasi menjadi spasi
        # Jumlah spasi harus dibedakan agar Pandas tidak error (unik)
        "_1": " ",
        "_2": "  ",
        "POSISI": "   ",
        "_3": "    ",
        "_4": "     ",
        "_5": "      ",
        "_6": "       ",
        "DELTA": "        ",
        "_7": "         ",
        "_8": "          ",
        "_9": "           "
    }

    # Buat salinan dataframe khusus untuk ditampilkan, lalu rename nama kolomnya
    df_tampil = df_clean[kolom_final].rename(columns=rename_mapping)

    # GROUPING KOLOM (MULTI-INDEX HEADER)
    # Pasangkan nama kolom yang sudah menjadi spasi tadi ke "DATA REALISASI"
    header_mapping = {
        # Semua spasi kosong dimasukkan ke grup yang sama
        " ": "DATA REALISASI",
        "  ": "DATA REALISASI",
        "   ": "DATA REALISASI",
        "    ": "DATA REALISASI",
        "     ": "DATA REALISASI",
        "      ": "DATA REALISASI",
        "       ": "DATA REALISASI",
        
        "        ": "delta",
        "         ": "delta",
        "          ": "delta",
        "           ": "delta",
        
        alias_rka: f"KINERJA {nama_bulan_ini}",       
        alias_gap: f"KINERJA {nama_bulan_ini}",        
        alias_pencapaian: f"KINERJA {nama_bulan_ini}"  
    }

    # Proses Multi-Index
    multi_index_tuples = []
    for col in df_tampil.columns:
        grup_atas = header_mapping.get(col, "LAINNYA") 
        multi_index_tuples.append((grup_atas, col))

    df_tampil.columns = pd.MultiIndex.from_tuples(multi_index_tuples)
    df_tampil = df_tampil.iloc[:35]

    def parse_pencapaian_number(raw_value):
        text = str(raw_value).strip()
        try:
            return float(text.replace("%", "").replace(",", "."))
        except Exception:
            return None

    def highlight_pencapaian_cell(value):
        text = str(value).strip()
        numeric = parse_pencapaian_number(text)

        if numeric is None:
            background = "#F3F4F6"
            color = "#111827"
        elif numeric < 95:
            background = "#FEE2E2"
            color = "#991B1B"
        elif numeric < 100:
            background = "#FEF3C7"
            color = "#92400E"
        else:
            background = "#DCFCE7"
            color = "#166534"

        return (
            f"background:{background};"
            f" color:{color};"
            f" border-radius:14px;"
            f" padding:4px 10px;"
            f" font-weight:600;"
        )
