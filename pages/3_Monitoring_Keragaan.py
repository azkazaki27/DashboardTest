import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Monitoring Keragaan",
    layout="wide"
)

from utils.style import load_css

load_css()

import base64

# =====================================
# ENCODE LOGO
# =====================================



# =====================================
# IMPORT
# =====================================

from utils.load_data import (
    load_data,
    sheet_mapping
)

# =====================================
# TITLE
# =====================================

st.title("Monitoring Keragaan")

# =====================================
# KPI WARNING FUNCTION
# =====================================

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

        # ====================
        # HEADER
        # ====================

        if "TOTAL PINJAMAN" in nama:

            current_kelompok = "TOTAL PINJAMAN"

        elif "TOTAL SML" in nama:

            current_kelompok = "TOTAL SML"

        elif "TOTAL NPL" in nama:

            current_kelompok = "TOTAL NPL"

        elif "TOTAL DPK" in nama:

            current_kelompok = "TOTAL DPK"
                # ====================
                # DETAIL DPK
                # ====================

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

        # ====================
        # PINJAMAN / SML / NPL
        # ====================

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

# =====================================
# PILIH KANTOR
# =====================================

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
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%Y-%m-%d",
            "%d %B %Y",
            "%d %b %Y",
            "%Y/%m/%d"
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
        row0 = df.iloc[0].fillna("").astype(str)

        # First choose direct prefix matches like RKA, GAP RKA, or PENCAPAIAN RKA
        candidates = [
            col for col in df.columns
            if col == prefix or col.startswith(prefix + "_")
        ]

        matching = [
            col for col in candidates
            if row0.get(col, "").strip() == month_label
        ]
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
                if row0.get(col, "").strip() == month_label
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
    
    # =====================================
    # WARNING KPI
    # =====================================

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

        if selected_kantor == "KCP BTC":

            allowed = [

                ("TOTAL PINJAMAN", "Small"),

                ("TOTAL SML", "Small"),
                ("TOTAL SML", "Micro"),

                ("TOTAL NPL", "Small"),

                ("TOTAL DPK", "Tabungan"),
                ("TOTAL DPK", "Giro"),
                ("TOTAL DPK", "Deposito")
            ]

        elif selected_kantor in ["KCP Bintaro", "KCP Graha"]:

            allowed = [

                ("TOTAL PINJAMAN", "Small"),

                ("TOTAL SML", "Small"),
                ("TOTAL SML", "Micro"),

                ("TOTAL NPL", "Small"),
                ("TOTAL NPL", "Micro"),

                ("TOTAL DPK", "Tabungan"),
                ("TOTAL DPK", "Giro"),
                ("TOTAL DPK", "Deposito")
            ]

        else:

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

    # =====================================
    # DASHBOARD KPI
    # =====================================

    col_warning, col_chart = st.columns([50, 50])

    # =====================================
    # WARNING KPI (KIRI)
    # =====================================

    with col_warning:

        c1, c2, c3 = st.columns(3)

        # =====================
        # MERAH
        # =====================

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
                ">
                    <h4 style="color:#111827;font-size:14px;margin:0 0 8px 0;">
                        🔴 Perlu Perhatian ({len(merah)})
                    </h4>
                    {html}
                </div>
                """,
                unsafe_allow_html=True
            )

        # =====================
        # KUNING
        # =====================

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
                ">
                    <h4 style="color:#111827;font-size:14px;margin:0 0 8px 0;">
                        🟡 Mendekati Target ({len(kuning)})
                    </h4>
                    {html}
                </div>
                """,
                unsafe_allow_html=True
            )

        # =====================
        # HIJAU
        # =====================

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
                ">
                    <h4 style="color:#111827;font-size:14px;margin:0 0 8px 0;">
                        🟢 Memenuhi Target ({len(hijau)})
                    </h4>
                    {html}
                </div>
                """,
                unsafe_allow_html=True
            )

    # =====================================
    # GRAFIK KPI (KANAN)
    # =====================================

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
            return ["", "", "", "", "", "", ""]

        ytd = row.get("DELTA", "")
        mtd = row.get("_7", "")
        dtd = row.get("_8", "")
        yoy = row.get("_9", "")
        rka = row.get(kolom_asli_rka, "") if kolom_asli_rka else ""
        gap = row.get(kolom_asli_gap, "") if kolom_asli_gap else ""
        pencapaian = row.get(kolom_asli_pencapaian, "") if kolom_asli_pencapaian else ""
        return [ytd, mtd, dtd, yoy, rka, gap, pencapaian]

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
                f" background:{background}; color:{color}; font-weight:700; font-size:20px; line-height:1.1;"
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
            return f"<div style='font-size:20px; font-weight:700; color:{color};'>{text}</div>"

        values = get_row_metrics(row)
        st.subheader(title)
        cols = st.columns(7)
        for idx, label in enumerate(["YTD", "MTD", "DTD", "YOY", "RKA", "GAP RKA", "PENCAPAIAN RKA"]):
            cols[idx].markdown(
                f"<div style='font-size:14px; font-weight:600; color:#1F2937; margin-bottom:4px;'>{label}</div>"
                + format_value(values[idx], label),
                unsafe_allow_html=True
            )

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
                "TOTAL PINJAMAN": ["A."],
                "TOTAL SML": ["A.", "C."],
                "TOTAL NPL": ["A."]
            },
            "KCP Bintaro": {
                "TOTAL PINJAMAN": ["A."],
                "TOTAL SML": ["A.", "C."],
                "TOTAL NPL": ["A.", "C."]
            },
            "KCP Graha": {
                "TOTAL PINJAMAN": ["A."],
                "TOTAL SML": ["A.", "C."],
                "TOTAL NPL": ["A.", "C."]
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
                numeric = float(
                    text.replace("%", "").replace(",", ".").strip()
                )
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
                f" min-height:16px; padding:2px 6px; border-radius:14px;"
                f" background:{background}; color:{color}; font-weight:600;"
                f" font-size:inherit; line-height:1.1; vertical-align:middle; text-align:right;'>"
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
            return f"<span style='color:{color};'>{text}</span>"

        # Map column names to display names
        col_mapping = {
            "DELTA": "YTD",
            "_7": "MTD",
            "_8": "DTD",
            "_9": "YOY",
            kolom_asli_rka: "RKA",
            kolom_asli_gap: "GAP RKA",
            kolom_asli_pencapaian: "PENCAPAIAN RKA"
        }

        # Contextual label maps per parent total
        parent_label_map = {
            "TOTAL DPK": {
                "tabungan": "Tabungan",
                "TABUNGAN": "Tabungan",
                "giro": "Giro",
                "GIRO": "Giro",
                "deposito": "Deposito",
                "DEPOSITO": "Deposito"
            },
        }

        # Filter cols_to_show to only those that exist in dataframe
        available_cols = [c for c in cols_to_show if c in detail_df.columns]

        # Extract metric columns (skip MATA ANGGARAN)
        metric_cols = available_cols[1:]
        metric_labels = [col_mapping.get(c, c) for c in metric_cols]

        # Display header (Item column larger; metric headers slightly smaller)
        header_cols = st.columns([2] + [1] * len(metric_labels))
        header_cols[0].markdown("<div style='font-size:10px; font-weight:700; color:#111827; margin-bottom:4px;'>Item</div>", unsafe_allow_html=True)
        for i, label in enumerate(metric_labels):
            header_cols[i + 1].markdown(f"<div style='text-align: right; font-size:10px;'><b>{label}</b></div>", unsafe_allow_html=True)

        # Display each row (Item text bigger; values slightly smaller to keep visual gap)
        for idx, row in detail_df[available_cols].iterrows():
            raw_item = str(row.iloc[0]).strip()

            # For DPK, use _2 column value if available
            if parent_total == "TOTAL DPK" and "_2" in detail_df.columns:
                raw_item = str(detail_df.iloc[idx]["_2"]).strip()

            raw_item_lower = raw_item.lower().strip()

            # apply contextual mapping if exists
            if parent_total and parent_total in parent_label_map:
                # Try lowercase match first
                item_name = parent_label_map[parent_total].get(raw_item_lower)
                if not item_name:
                    # Try original case
                    item_name = parent_label_map[parent_total].get(raw_item)
                if not item_name:
                    item_name = get_item_label(raw_item)
            else:
                item_name = get_item_label(raw_item)

            row_cols = st.columns([2] + [1] * len(metric_labels))
            # Item column larger and slightly bolder
            row_cols[0].markdown(f"<div style='font-size:14px; font-weight:600; color:#111827;'>{item_name}</div>", unsafe_allow_html=True)
            for i in range(len(metric_labels)):
                value = row.iloc[i + 1]
                label = metric_labels[i]
                colored_value = format_value_color(value, label)
                # Values have slightly smaller font to maintain hierarchy and gap
                row_cols[i + 1].markdown(f"<div style='text-align: right; font-size:13px;'>{colored_value}</div>", unsafe_allow_html=True)

    cols_to_display = ["MATA ANGGARAN", "DELTA", "_7", "_8", "_9"]
    if kolom_asli_rka and kolom_asli_rka in df_clean.columns:
        cols_to_display.append(kolom_asli_rka)
    if kolom_asli_gap and kolom_asli_gap in df_clean.columns:
        cols_to_display.append(kolom_asli_gap)
    if kolom_asli_pencapaian and kolom_asli_pencapaian in df_clean.columns:
        cols_to_display.append(kolom_asli_pencapaian)

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

    # =====================================
    # FILTER & TAMPILKAN
    # =====================================

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

    # =====================================
    # GROUPING KOLOM (MULTI-INDEX HEADER)
    # =====================================

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

    # Apply styling only if PENCAPAIAN RKA exists in flat columns (not MultiIndex)
    styled_df = df_tampil
    if not isinstance(df_tampil.columns, pd.MultiIndex) and alias_pencapaian in df_tampil.columns:
        try:
            styled_df = df_tampil.style.applymap(
                highlight_pencapaian_cell,
                subset=alias_pencapaian
            )
        except (KeyError, Exception):
            styled_df = df_tampil

    st.write(styled_df)
