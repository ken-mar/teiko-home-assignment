# Teiko Home Assignment

## How to Run
```bash
make setup
make pipeline
make dashboard
```

> In GitHub Codespaces, after `make dashboard` open the forwarded port 8501.

## Database Schema

### Tables
- **projects** — one row per clinical project
- **subjects** — one row per patient, linked to a project
- **samples** — one row per blood draw (timepoint), linked to a subject
- **populations** — lookup table for the 5 cell types
- **sample_counts** — one row per sample+population pair, stores the count

### Relationships
```
projects → subjects → samples → sample_counts ← populations
```

### Why this design?
Cell counts are stored in long format rather than wide format. This makes aggregations clean, and adding new cell types requires no schema changes. Subject-level attributes (age, sex, treatment, response) live in `subjects` to avoid repeating them across timepoints.

### Scaling
| Challenge | How it's handled |
|---|---|
| More projects | New rows in `projects`, no schema change |
| More subjects/samples | Indexed foreign keys keep queries fast |
| New cell populations | New rows in `populations`, no schema change |
| New analytics | Views or new tables built on top of `sample_counts` |

## Code Structure

- `load_data.py` — creates the SQLite schema and loads `cell-count.csv`
- `pipeline.py` — runs Parts 2-4: summary table, statistics, boxplot, subset queries
- `dashboard.py` — Streamlit dashboard displaying all outputs
- `outputs/` — generated files: summary table, boxplot, stats results, subset answers

## Notes
- quintazide is flagged as a future treatment of interest for exploratory modeling
- No life sciences background required to run or extend this project

## Dashboard
<!-- TODO -->
