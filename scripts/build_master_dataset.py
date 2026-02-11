from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import get_config
from src.data.load_raw import (
    load_ff_factors_csv,
    load_industry_49_xlsx,
    load_spy_agg_stacked_csv,
    load_vix_csv,
)


START_DATE = "2003-09-20"
END_DATE = "2024-12-31"


def main() -> None:
    cfg = get_config()

    raw_dir = cfg.data_raw
    out_dir = cfg.data_processed
    out_dir.mkdir(parents=True, exist_ok=True)

    ret = load_spy_agg_stacked_csv(raw_dir / "SPYAGG.csv")
    ff = load_ff_factors_csv(raw_dir / "RF.csv")
    ind = load_industry_49_xlsx(raw_dir / "49.xlsx")

    vix_path = raw_dir / "VIX.csv"
    vix = load_vix_csv(vix_path) if vix_path.exists() else None

    ret = ret.loc[START_DATE:END_DATE]
    ff = ff.loc[START_DATE:END_DATE]
    ind = ind.loc[START_DATE:END_DATE]
    if vix is not None:
        vix = vix.loc[START_DATE:END_DATE]


    print("RET:", ret.shape, ret.index.min(), ret.index.max())
    print("FF :", ff.shape, ff.index.min(), ff.index.max())
    print("IND:", ind.shape, ind.index.min(), ind.index.max())
    print("VIX:", None if vix is None else (vix.shape, vix.index.min(), vix.index.max()))

    # Notes (GPT)
    # ret, ff are decimals already; ind is % (your std~1.56 confirms).
    # We do NOT convert in this script unless you want.
    # If you want consistent decimals now, uncomment the next line:
    ind = ind / 100.0

    master = ret.join(ff, how="inner").join(ind, how="inner")
    if vix is not None:
        master = master.join(vix, how="left")

    print("MASTER:", master.shape, master.index.min(), master.index.max())
    print("\nMissing values (total):", int(master.isna().sum().sum()))
    print("\nColumns:", list(master.columns[:10]), "...")
    print("\nRET dtypes:", master[["SPY_RET", "AGG_RET"]].dtypes)

    master_path = out_dir / "master_daily_2003_2024.csv"
    master.to_csv(master_path)
    print("\nWrote:", master_path)

    ret.to_csv(out_dir / "returns_spy_agg.csv")
    ff.to_csv(out_dir / "ff_factors.csv")
    ind.to_csv(out_dir / "ff_industry_49.csv")
    if vix is not None:
        vix.to_csv(out_dir / "vix.csv")


if __name__ == "__main__":
    main()