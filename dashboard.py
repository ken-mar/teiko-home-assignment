import json
import pandas as pd
import streamlit as st

OUTPUTS_DIR = "outputs"

st.set_page_config(page_title="Teiko Immune Profiling", layout="wide")
st.title("Teiko — Immune Cell Profiling Dashboard")

# Part 2
st.header("Part 2 — Cell Population Frequencies")
summary_df = pd.read_csv(f"{OUTPUTS_DIR}/summary_table.csv")
st.dataframe(summary_df)

# Part 3
st.header("Part 3 — Responder vs Non-Responder")
st.image(f"{OUTPUTS_DIR}/boxplot.png", use_column_width=True)
stats_df = pd.read_csv(f"{OUTPUTS_DIR}/stats_results.csv")
st.dataframe(stats_df)

# Part 4
st.header("Part 4 — Baseline Subset Analysis")
with open(f"{OUTPUTS_DIR}/subset_answers.json") as f:
    answers = json.load(f)
st.json(answers)