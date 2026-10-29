import pandas as pd

df = pd.read_csv(
    "../data/prediction_Q.csv"
)

threshold = 0.5

print()
print("===== Q Prediction Summary =====")
print()

for col in [
    "detectable",
    "bright_neighbor",
    "multiple_component",
    "point_source"
]:

    count = (df[col] >= threshold).sum()

    frac = count / len(df) * 100

    print(
        f"{col:20s}"
        f"{count:5d} "
        f"({frac:.1f}%)"
    )

print()
print(
    f"Total Objects : {len(df)}"
)