import sqlite3
import pandas as pd

DB_PATH = "teiko.db"
CSV_PATH = "cell-count.csv"

POPULATIONS = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]


def create_schema(conn: sqlite3.Connection) -> None:
    pass


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
