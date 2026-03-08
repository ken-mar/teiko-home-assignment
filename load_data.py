import sqlite3
import pandas as pd

DB_PATH = "teiko.db"
CSV_PATH = "cell-count.csv"

POPULATIONS = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]


def create_schema(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()

    cursor.execute("""  
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""  
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id  TEXT PRIMARY KEY,
            project_id  INTEGER NOT NULL REFERENCES projects(project_id),
            condition   TEXT,
            age         INTEGER,
            sex         TEXT,
            treatment   TEXT,
            response    TEXT
        )
    """)

    cursor.execute("""  
        CREATE TABLE IF NOT EXISTS samples (
            sample_id                   TEXT PRIMARY KEY,
            subject_id                  TEXT NOT NULL REFERENCES subjects(subject_id),
            sample_type                 TEXT,
            time_from_treatment_start   INTEGER   
        )
    """)

    cursor.execute("""  
        CREATE TABLE IF NOT EXISTS populations (
            population_id INTEGER PRIMARY KEY,
            name           TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""  
        CREATE TABLE IF NOT EXISTS sample_counts (
            sample_id       TEXT NOT NULL REFERENCES samples(sample_id),
            population_id   INTEGER NOT NULL REFERENCES populations(population_id),
            count           INTEGER NOT NULL,
            PRIMARY KEY (sample_id, population_id)
        )
    """)
    conn.commit()


def load_csv(conn: sqlite3.Connection, csv_path: str) -> None:
    pass


def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        create_schema(conn)
        load_csv(conn, CSV_PATH)
        print(f"Database created: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
