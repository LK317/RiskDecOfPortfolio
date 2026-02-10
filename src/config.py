from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ProjectConfig:
    root: Path
    data_raw: Path
    data_processed: Path

    start_date: str = "2000-01-01"
    end_date: str = "2026-12-31"  # todo: to latest availiable

    tickers: tuple[str, ...] = ("SPY", "AGG")

def get_config() -> ProjectConfig:
    root = Path(__file__).resolve().parents[1]
    return ProjectConfig(
        root=root,
        data_raw=root / "data" / "raw",
        data_processed=root / "data" / "processed",
    )