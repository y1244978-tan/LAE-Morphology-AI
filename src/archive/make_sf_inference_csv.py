import pandas as pd

df = pd.read_csv(
    "../data/catalog_nonLAE_SF_F277W_with_err_kpc.txt",
    sep=r"\s+",
    encoding="cp932"
)

exclude_ids = [
    718922,
    1103622
]

df = df[
    ~df["ID"].isin(exclude_ids)
]

out = pd.DataFrame()

out["id"] = df["ID"]

out["detectable"] = 0
out["bright_neighbor"] = 0
out["multiple_component"] = 0
out["point_source"] = 0

out.to_csv(
    "../data/sf_inference.csv",
    index=False
)

print(
    f"SF inference csv saved ({len(out)})"
)