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
    query = """
        WITH totals AS (
            SELECT sample_id, SUM(count) as total_count
            FROM sample_counts
            GROUP BY sample_id
        )
        SELECT
            s.sample_id     as sample,
            t.total_count   as total_count,
            p.name          as population,
            sc.count        as count,
            ROUND(100.0 * sc.count / t.total_count, 2)  as percentage
        FROM samples s
        JOIN totals t          ON s.sample_id = t.sample_id
        JOIN sample_counts sc  ON s.sample_id = sc.sample_id
        JOIN populations p     ON sc.population_id = p.population_id
    """
    return pd.read_sql_query(query, conn)

def get_melanoma_miraclib_pbmc(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
        WITH totals AS (
            SELECT sample_id, SUM(count) as total_count
            FROM sample_counts
            GROUP BY sample_id
        )
        SELECT
            sb.subject_id   as subject_id,
            s.sample_id     as sample,
            p.name          as population,
            ROUND(100.0 * sc.count / t.total_count, 2)  as percentage,
            sb.response     as response
        FROM samples s
        JOIN subjects sb       ON s.subject_id = sb.subject_id
        JOIN totals t          ON s.sample_id = t.sample_id
        JOIN sample_counts sc  ON s.sample_id = sc.sample_id
        JOIN populations p     ON sc.population_id = p.population_id
        WHERE sb.condition = 'melanoma'
          AND sb.treatment = 'miraclib'
          AND s.sample_type = 'PBMC'
          AND sb.response IS NOT NULL
    """
    return pd.read_sql_query(query, conn)

def run_statistics(df: pd.DataFrame) -> pd.DataFrame:
    results = []
    for p in POPULATIONS:
        p_df = df[df['population'] == p]
        responders = p_df[p_df['response'] == 'yes']['percentage']
        non_responders = p_df[p_df['response'] == 'no']['percentage']

        stat, p_value = mannwhitneyu(responders, non_responders, alternative='two-sided')

        results.append({
            'population': p,
            'n_resp': len(responders),
            'n_non': len(non_responders),
            'median_resp': round(responders.median(), 2),
            'median_non': round(non_responders.median(), 2),
            'p_value': round(p_value, 4)
        })

    stats_df = pd.DataFrame(results)

    _, p_adj, _, _ = multipletests(stats_df['p_value'], method='fdr_bh')
    stats_df['p_adj'] = p_adj.round(4)
    stats_df['significant'] = stats_df['p_adj'] < 0.05

    return stats_df


def make_boxplot(df: pd.DataFrame) -> None:
    pass


def run_subset_queries(conn: sqlite3.Connection) -> dict:
    pass


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        summary_df = get_summary_table(conn)
        summary_df.to_csv(f"{OUTPUTS_DIR}/summary_table.csv", index=False)

        # TODO: uncomment after each stub is complete
        analysis_df = get_melanoma_miraclib_pbmc(conn)
        stats_df = run_statistics(analysis_df)
        stats_df.to_csv(f"{OUTPUTS_DIR}/stats_results.csv", index=False)
        # make_boxplot(analysis_df)

        # answers = run_subset_queries(conn)
        # with open(f"{OUTPUTS_DIR}/subset_answers.json", "w") as f:
        #     json.dump(answers, f, indent=2)

        print("Pipeline complete.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
