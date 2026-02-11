from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
import numpy as np
import pandas as pd

### Forall desc check 01_data_overview in notebooks folder
FF_MISSING = (-99.99, -999)


def _dedupe_columns(cols: List[str]) -> List[str]:
    seen: Dict[str, int] = {}
    out: List[str] = []
    for c in cols:
        c = str(c)
        if c not in seen:
            seen[c] = 0
            out.append(c)
        else:
            seen[c] += 1
            out.append(f"{c}.{seen[c]}")
    return out


def load_spy_agg_stacked_csv(path: Path) -> pd.DataFrame:

    df = pd.read_csv(path, parse_dates=["date"])
    df = df.set_index("date").sort_index()

    df["RET"] = pd.to_numeric(df["RET"], errors="coerce")

    wide = (
        df[["PERMNO", "RET"]]
        .reset_index()
        .pivot(index="date", columns="PERMNO", values="RET")
        .sort_index()
    )

    starts = wide.apply(lambda s: s.first_valid_index())
    permno_spy = starts.idxmin()
    permno_agg = starts.idxmax()

    ret = wide.rename(columns={permno_spy: "SPY_RET", permno_agg: "AGG_RET"})
    return ret


def load_ff_factors_csv(path: Path) -> pd.DataFrame:
    ff = pd.read_csv(path, parse_dates=["date"])
    ff = ff.set_index("date").sort_index()
    return ff


def load_industry_49_xlsx(path: Path) -> pd.DataFrame:
    import numpy as np
    import pandas as pd

    ind = pd.read_excel(path)

    first_col = ind.columns[0]
    ind = ind.rename(columns={first_col: "date"})

    d = ind["date"]

    if np.issubdtype(d.dtype, np.datetime64):
        ind["date"] = pd.to_datetime(d, errors="coerce")
    else:
        s = d.astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
        ind["date"] = pd.to_datetime(s, format="%Y%m%d", errors="coerce")

    ind = ind.dropna(subset=["date"]).set_index("date").sort_index()

    ind = ind.apply(pd.to_numeric, errors="coerce")
    ind = ind.replace([-99.99, -999], np.nan)

    return ind


def load_vix_csv(path: Path) -> pd.DataFrame:

    vix = pd.read_csv(path, parse_dates=["Date"])
    cols = [c for c in vix.columns if c in ("Date", "VIX")]
    vix = vix[cols].dropna(subset=["VIX"])
    vix = vix.drop_duplicates(subset=["Date"], keep="last")
    vix = vix.set_index("Date").sort_index()
    vix.index.name = "date"
    return vix