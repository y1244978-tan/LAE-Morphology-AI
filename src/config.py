from pathlib import Path

csv_files = sorted(
    Path("../data").glob(
        "morphology_labels_*.csv"
    )
)

CSV_FILE = str(csv_files[-1])

print(
    f"Using CSV: {csv_files[-1].name}"
)
