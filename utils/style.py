import streamlit as st

def load_css():

    st.markdown("""
    <style>
    
    /* =====================================
    SIDEBAR NAVIGATION
    ===================================== */
    
    [data-testid="stSidebarNav"] {
    
        margin-top: 10px;
    }
    
/* =====================================
SIDEBAR
===================================== */

section[data-testid="stSidebar"] {

    background-color: #00529C;

    position: relative;
}

/* =====================================
SEMBUNYIKAN HEADER DEFAULT NAV
===================================== */

[data-testid="stSidebarNav"] {

    padding-top: 18px !important;
}

/* =====================================
LOGO CUSTOM
===================================== */

.sidebar-logo {

    position: absolute;

    top: 5px;

    left: 10px;
                

    width: 190px;

    z-index: 999999;
}

    /* =====================================
    GLOBAL
    ===================================== */

    .stApp {

        background-color: #F4F7FB;

        color: #1F2937;
        font-size: 14px;
    }

    /* =====================================
    MAIN CONTAINER - RESPONSIVE
    ===================================== */

    .main .block-container {

        max-width: 100%;

        padding-top: 0.75rem;

        padding-left: 1rem;

        padding-right: 1rem;
    }

    @media (min-width: 768px) {
        .main .block-container {
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
    }

    @media (min-width: 1024px) {
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    }

    /* =====================================
    SIDEBAR
    ===================================== */

    section[data-testid="stSidebar"] {

        background: linear-gradient(
            180deg,
            #00529C 0%,
            #0B3B6E 100%
        );
    }

    section[data-testid="stSidebar"] * {

        color: white !important;

        font-size: 14px !important;
    }

    /* =====================================
    TITLE - RESPONSIVE
    ===================================== */

    h1 {
        color: #00529C !important;
        font-weight: 700 !important;
        font-size: 28px !important;
        margin-bottom: 0.75rem !important;
        margin-top: 0.5rem !important;
    }

    h2 {
        color: #00529C !important;
        font-weight: 700 !important;
        font-size: 22px !important;
        margin-bottom: 0.5rem !important;
        margin-top: 0.4rem !important;
    }

    h3 {
        color: #00529C !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        margin-bottom: 0.5rem !important;
        margin-top: 0.3rem !important;
    }

    h4 {
        color: #00529C !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        margin-bottom: 0.3rem !important;
    }

    @media (max-width: 768px) {
        h1 {
            font-size: 24px !important;
        }
        h2 {
            font-size: 20px !important;
        }
        h3 {
            font-size: 16px !important;
        }
    }

    /* =====================================
    STREAMLIT DATAFRAME
    ===================================== */

    [data-testid="stDataFrame"] {

        width: 100% !important;

        background: white !important;

        border-radius: 12px !important;

        border: 1px solid #DCE6F2 !important;

        padding: 6px !important;

        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    /* =====================================
    DATA EDITOR
    ===================================== */

    [data-testid="stDataEditor"] {

        width: 100% !important;

        background: white !important;

        border-radius: 12px !important;

        border: 1px solid #DCE6F2 !important;
    }

    /* =====================================
    REMOVE DARK GRID
    ===================================== */

    [data-testid="stDataFrame"] div[role="grid"] {

        background-color: white !important;
    }

    /* =====================================
    COLUMNS - COMPACT GAPS
    ===================================== */

    [data-testid="column"] {
        gap: 4px !important;
    }

    /* =====================================
    PILLS CONTAINER - COMPACT GAPS
    ===================================== */

    div[data-baseweb="button-group"] {

        gap: 6px !important;
    }

    /* =====================================
    DEFAULT BUTTON - SMALLER
    ===================================== */

    div[data-baseweb="button-group"] button {

        background-color: #F3F4F6 !important;

        color: #374151 !important;

        border: 1px solid #D1D5DB !important;

        border-radius: 18px !important;

        padding: 5px 14px !important;

        font-weight: 600 !important;

        font-size: 13px !important;

        transition: all 0.2s ease !important;
    }

    /* =====================================
    HOVER BUTTON
    ===================================== */

    div[data-baseweb="button-group"] button:hover {

        background-color: #DCFCE7 !important;

        color: #166534 !important;

        border-color: #22C55E !important;
    }

    /* =====================================
    ACTIVE BUTTON
    ===================================== */

    div[data-baseweb="button-group"] button[aria-pressed="true"] {

        background-color: #22C55E !important;

        color: white !important;

        border: 1px solid #22C55E !important;

        box-shadow: 0 2px 6px rgba(34,197,94,0.2) !important;

        font-weight: 700 !important;
    }

    /* =====================================
    ACTIVE BUTTON HOVER
    ===================================== */

    div[data-baseweb="button-group"] button[aria-pressed="true"]:hover {

        background-color: #16A34A !important;

        border-color: #16A34A !important;

        color: white !important;
    }

    /* =====================================
    PRIMARY BUTTON - SMALLER
    ===================================== */

    .stButton > button {

        background-color: #22C55E !important;

        color: white !important;

        border: none !important;

        border-radius: 8px !important;

        font-weight: 700 !important;

        padding: 8px 14px !important;

        font-size: 13px !important;

        transition: 0.2s ease !important;
    }

    .stButton > button:hover {

        background-color: #16A34A !important;

        color: white !important;
    }

    /* =====================================
    METRIC CARDS - COMPACT
    ===================================== */

    [data-testid="metric-container"] {

        color: #00529C !important;
        padding: 0.75rem 1rem !important;
    }

    [data-testid="metric-container"] span,
    [data-testid="metric-container"] div {

        color: #00529C !important;
    }

    /* Metric value font size */
    [data-testid="metric-container"] [data-testid="metric-container-0"] > div:first-child {
        font-size: 22px !important;
    }

    /* =====================================
    TABLE WRAPPER - COMPACT
    ===================================== */

 .table-wrapper {

    width: 100%;

    overflow-x: auto;

    overflow-y: hidden;

    background: white;

    border-radius: 12px;

    border: 1px solid #DCE6F2;

    box-shadow: 0 2px 8px rgba(0,0,0,0.03);

    margin-top: 12px;

    margin-bottom: 12px;

    padding-bottom: 8px;
}

    /* =====================================
    CUSTOM TABLE - COMPACT
    ===================================== */

    .custom-table {

        width: 100% !important;

        min-width: 100%;

        border-collapse: collapse;

        font-size: 12px !important;

        white-space: nowrap;

        background: white;
    }

    /* =====================================
    TABLE HEADER - COMPACT
    ===================================== */

    .custom-table thead th {

        position: sticky;

        top: 0;

        z-index: 10;

        background: linear-gradient(
            180deg,
            #0A5EB0 0%,
            #00529C 100%
        ) !important;

        color: white !important;

        padding: 8px 6px !important;

        text-align: center;

        font-weight: 700;

        font-size: 12px !important;

        border: 1px solid #D1D5DB;
    }

    /* =====================================
    TABLE BODY - COMPACT
    ===================================== */

    .custom-table tbody td {

        padding: 6px 5px !important;

        border: 1px solid #E5E7EB;

        color: #1F2937;

        text-align: right;

        font-size: 12px !important;
    }

    /* =====================================
    FIRST COLUMN
    ===================================== */

    .custom-table tbody td:first-child {

        text-align: left;

        font-weight: 600;
    }

    /* =====================================
    ZEBRA ROW
    ===================================== */

    .custom-table tbody tr:nth-child(even) {

        background-color: #F8FBFF;
    }

    /* =====================================
    ROW HOVER
    ===================================== */

    .custom-table tbody tr:hover {

        background-color: #EAF4FF;
    }

    /* =====================================
    ALERT / NOTIFICATION - COMPACT
    ===================================== */

    div[data-baseweb="notification"] {

        border-radius: 10px !important;

        padding: 12px 16px !important;

        font-size: 13px !important;
    }

    div[data-baseweb="notification"] p {
        font-size: 13px !important;
        margin: 0px !important;
    }


    /* =====================================
    SCROLLBAR
    ===================================== */

    ::-webkit-scrollbar {

        width: 8px;

        height: 8px;
    }

    ::-webkit-scrollbar-thumb {

        background: #A0AEC0;

        border-radius: 8px;
    }

    ::-webkit-scrollbar-track {

        background: #F0F2F5;
    }
    
    /* =====================================
TABLE FIX
===================================== */

.table-wrapper table {

    border-collapse: collapse !important;

    width: 100% !important;

    min-width: 100% !important;
}

.table-wrapper th,
.table-wrapper td {

    white-space: nowrap;
}

/* =====================================
DATAFRAME - COMPACT
===================================== */

[data-testid="stDataFrame"] {

    border-radius: 12px !important;

    border: 1px solid #D1D5DB !important;

    overflow: auto !important;
}

/* =====================================
HEADER TABLE - COMPACT
===================================== */

[data-testid="stDataFrame"] thead tr th {

    background-color: #00529C !important;

    color: white !important;

    font-weight: 700 !important;

    font-size: 12px !important;

    text-align: center !important;

    padding: 8px 6px !important;
}

/* =====================================
BODY TABLE - COMPACT
===================================== */

[data-testid="stDataFrame"] tbody tr td {

    background-color: white !important;

    color: #1F2937 !important;

    font-size: 12px !important;

    padding: 6px 5px !important;
}

/* =====================================
ZEBRA ROW
===================================== */

[data-testid="stDataFrame"] tbody tr:nth-child(even) td {

    background-color: #F8FBFF !important;
}

/* =====================================
WARNING BOX TEXT - COMPACT
===================================== */

div[data-baseweb="notification"] {

    color: #111827 !important;
}

div[data-baseweb="notification"] p {

    color: #111827 !important;

    font-weight: 600 !important;

    font-size: 13px !important;

    margin: 0px !important;
}

div[data-baseweb="notification"] span {

    color: #111827 !important;
    font-size: 13px !important;
}

/* =====================================
EXPANDER - COMPACT
===================================== */

[data-testid="stExpander"] {
    font-size: 13px !important;
}

[data-testid="stExpander"] button {
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* =====================================
STREAMLIT TEXT - SMALLER
===================================== */

.stMarkdown {
    font-size: 14px !important;
}

p {
    font-size: 14px !important;
    line-height: 1.4 !important;
}

/* =====================================
RESPONSIVE ADJUSTMENTS
===================================== */

@media (max-width: 640px) {
    .main .block-container {
        padding-top: 0.5rem;
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }
    
    h1 {
        font-size: 20px !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        font-size: 17px !important;
    }
    
    h3 {
        font-size: 15px !important;
    }
    
    .custom-table {
        font-size: 11px !important;
    }
    
    [data-testid="stDataFrame"] tbody tr td {
        font-size: 11px !important;
        padding: 4px 3px !important;
    }
}

    </style>
    """, unsafe_allow_html=True)
