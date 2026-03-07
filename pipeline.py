import json
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

DB_PATH = "teiko.db"
OUTPUTS_DIR = "outputs"
POPULATIONS = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]


def get_summary_table(conn: sqlite3.Connection) -> pd.DataFrame:
    pass


def get_melanoma_miraclib_pbmc(conn: sqlite3.Connection) -> pd.DataFrame:
    pass


def run_statistics(df: pd.DataFrame) -> pd.DataFrame:
    pass


def make_boxplot(df: pd.DataFrame) -> None:
    pass


def run_subset_queries(conn: sqlite3.Connection) -> dict:
    pass


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        summary_df = get_summary_table(conn)
        summary_df.to_csv(f"{OUTPUTS_DIR}/summary_table.csv", index=False)

        analysis_df = get_melanoma_miraclib_pbmc(conn)
        stats_df = run_statistics(analysis_df)
        stats_df.to_csv(f"{OUTPUTS_DIR}/stats_results.csv", index=False)
        make_boxplot(analysis_df)

        answers = run_subset_queries(conn)
        with open(f"{OUTPUTS_DIR}/subset_answers.json", "w") as f:
            json.dump(answers, f, indent=2)

        print("Pipeline complete.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
