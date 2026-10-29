import pandas as pd

df = pd.read_csv(
    "../data/catalog_nonLAE_Q_F277W_with_err_kpc.txt",
    sep=r"\s+",
    encoding="cp932"
)

out = pd.DataFrame()

out["id"] = df["ID"]

out["detectable"] = 0
out["bright_neighbor"] = 0
out["multiple_component"] = 0
out["point_source"] = 0

out.to_csv(
    "../data/q_inference.csv",
    index=False
)

print(
    f"Q inference csv saved ({len(out)})"
)