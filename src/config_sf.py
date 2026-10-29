from pathlib import Path

csv_files = sorted(
    Path("../data").glob(
        "morphology_labels_*.csv"
    )
)

CSV_FILE = "../data/sf_inference.csv"

print(
    f"Using CSV: {CSV_FILE}"
)