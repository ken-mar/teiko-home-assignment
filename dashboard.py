import json
import pandas as pd
import streamlit as st

OUTPUTS_DIR = "outputs"

st.set_page_config(page_title="Teiko Immune Profiling", layout="wide")
st.title("Teiko — Immune Cell Profiling Dashboard")


@st.cache_data
def load_summary() -> pd.DataFrame:
    return pd.read_csv(f"{OUTPUTS_DIR}/summary_table.csv")


@st.cache_data
def load_stats() -> pd.DataFrame:
    return pd.read_csv(f"{OUTPUTS_DIR}/stats_results.csv")


@st.cache_data
def load_subset_answers() -> dict:
    with open(f"{OUTPUTS_DIR}/subset_answers.json") as f:
        return json.load(f)


st.header("Part 2 — Cell Population Frequencies")

st.header("Part 3 — Responder vs Non-Responder")

st.header("Part 4 — Baseline Subset Analysis")
