import pandas as pd
import re
from datetime import datetime

# =====================================
# GOOGLE SHEET
# =====================================

sheet_id = "1qvAL-ckHt7B_d-A-wy8vMyjYnTBEyd2jkN_thc8bn0M"

# =====================================
# SHEET MAPPING
# =====================================

sheet_mapping = {
    "Konsolidasi": "1282116519",
    "Kantor Cabang": "1111518864",
    "KCP BTC": "34445418",
    "KCP Bintaro": "1129781119",
    "KCP Graha": "895411510"
}

# =====================================
# HELPERS
# =====================================

def parse_indonesian_date(value):
    if value is None:
        return None

    value = str(value).strip()
    if not value:
        return None

    months = {
        "Januari": 1, "Februari": 2, "Maret": 3, "April": 4,
        "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8,
        "September": 9, "Oktober": 10, "November": 11, "Desember": 12
    }

    match = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", value)
    if not match:
        return None

    day, month_name, year = match.groups()
    month_num = months.get(month_name.capitalize())
    if not month_num:
        return None

    return datetime(int(year), month_num, int(day))


def find_sheet_date(df):
    if df.empty:
        return None

    first_row = df.iloc[0].fillna("").astype(str).tolist()

    for idx, cell in enumerate(first_row):
        if "TANGGAL" in cell.upper():
            if idx + 1 < len(first_row):
                parsed = parse_indonesian_date(first_row[idx + 1])
                if parsed:
                    return parsed
            parsed = parse_indonesian_date(cell)
            if parsed:
                return parsed

    for cell in first_row:
        parsed = parse_indonesian_date(cell)
        if parsed:
            return parsed

    return None


# =====================================
# LOAD DATA
# =====================================

def load_data(selected_kantor):

    gid = sheet_mapping[selected_kantor]

    url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{sheet_id}/export?format=csv&gid={gid}"
    )

    # =====================================
    # READ CSV
    # =====================================

    df = pd.read_csv(
        url,
        header=None,
        engine="python"
    )

    df = df.fillna("")

    sheet_date = find_sheet_date(df)

    # =====================================
    # HEADER ATAS & BAWAH
    # =====================================

    top_header = df.iloc[1]
    sub_header = df.iloc[2]

    columns = []

    current_top = ""

    # =====================================
    # BUILD HEADER
    # =====================================

    for top, sub in zip(top_header, sub_header):

        top = str(top).strip()
        sub = str(sub).strip()

        # Hilangkan unnamed
        if "Unnamed" in top:
            top = ""

        if "Unnamed" in sub:
            sub = ""

        # simpan header utama terakhir
        if top != "":
            current_top = top

        # =====================================
        # HEADER FINAL
        # =====================================

        # kalau hanya header utama
        if current_top != "" and sub == "":

            col_name = current_top

        # kalau ada subheader
        elif current_top != "" and sub != "":

            col_name = f"{current_top}_{sub}"

        # fallback
        else:

            col_name = sub

        columns.append(col_name)

    # =====================================
    # BUAT NAMA KOLOM UNIQUE
    # =====================================

    final_columns = []

    counts = {}

    for col in columns:

        if col not in counts:

            counts[col] = 0

            final_columns.append(col)

        else:

            counts[col] += 1

            final_columns.append(
                f"{col}_{counts[col]}"
            )

    # =====================================
    # SET HEADER
    # =====================================

    df.columns = [re.sub(r"^PERCAPAIAN RKA", "PENCAPAIAN RKA", col) for col in final_columns]

    # =====================================
    # HAPUS HEADER LAMA
    # =====================================

    df = df.iloc[3:]

    # =====================================
    # RESET INDEX
    # =====================================

    df = df.reset_index(drop=True)

    # =====================================
    # HAPUS KOLOM KOSONG
    # =====================================

    df = df.loc[
        :,
        ~df.columns.str.contains("^$")
    ]

    return df, sheet_date
