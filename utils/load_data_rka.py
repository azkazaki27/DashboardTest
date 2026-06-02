import pandas as pd

# =====================================
# GOOGLE SHEET
# =====================================

sheet_id = "1SxGYb9MA1UOwZgWZwg6MUO98ajiiG0g7H5TvA1Vl-7M"

# =====================================
# GID MAPPING
# =====================================

sheet_mapping = {
    "KONSOL BINTARO": "0",
    "SIMPANAN": "1207420112",
    "KREDIT": "633170900"
}

# =====================================
# CONVERT TO NUMBER
# =====================================

def convert_to_number(x):

    try:

        return float(
            str(x)
            .replace('.', '')
            .replace(',', '.')
        )

    except:

        return 0

# =====================================
# LOAD DATA
# =====================================

def load_data(selected_menu):

    # =====================================
    # AMBIL GID
    # =====================================

    gid = sheet_mapping[selected_menu]

    # =====================================
    # URL GOOGLE SHEET CSV
    # =====================================

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

    # =====================================
    # HILANGKAN NAN
    # =====================================

    df = df.fillna('')

    # =====================================
    # HAPUS BARIS KOSONG
    # =====================================

    df = df[
        ~(df == '').all(axis=1)
    ]

    # =====================================
    # RESET INDEX AWAL
    # =====================================

    df = df.reset_index(drop=True)

    # =====================================
    # HEADER DARI BARIS PERTAMA
    # =====================================

    df.columns = df.iloc[0]

    # Hilangkan nama header
    df.columns.name = None

    # =====================================
    # HAPUS BARIS HEADER LAMA
    # =====================================

    df = df[1:]

    # =====================================
    # RESET INDEX
    # =====================================

    df = df.reset_index(drop=True)

    # =====================================
    # RETURN DATA
    # =====================================

    return df
