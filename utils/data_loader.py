import pandas as pd
import numpy as np
import os


def _clean_rate(val):
    """Extract numeric rating from strings like '4.2/5'. Returns NaN for invalid values."""
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    if s in ("NEW", "-", "nan", ""):
        return np.nan
    try:
        return float(s.split("/")[0])
    except (ValueError, IndexError):
        return np.nan


def _clean_cost(val):
    """Remove commas and convert approx cost to float."""
    if pd.isna(val):
        return np.nan
    try:
        return float(str(val).replace(",", "").strip())
    except ValueError:
        return np.nan


def load_data(path: str = "data/zomato.csv") -> pd.DataFrame:
    """
    Load and clean the Zomato dataset.

    Parameters
    ----------
    path : str
        Path to the CSV file. Defaults to 'data/zomato.csv'.
        Falls back to 'data/sample_zomato.csv' if the primary file is not found.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe ready for analysis.
    """
    if not os.path.exists(path):
        fallback = os.path.join(os.path.dirname(path), "sample_zomato.csv")
        if os.path.exists(fallback):
            path = fallback
        else:
            raise FileNotFoundError(
                f"Data file not found at '{path}' or fallback '{fallback}'."
            )

    df = pd.read_csv(path)

    # Drop rows missing critical fields
    df.dropna(subset=["name", "location"], inplace=True)
    df = df[df["name"].str.strip() != ""]
    df = df[df["location"].str.strip() != ""]

    # Clean rate column
    df["rate"] = df["rate"].apply(_clean_rate)

    # Clean cost column
    cost_col = "approx_cost(for two people)"
    if cost_col in df.columns:
        df[cost_col] = df[cost_col].apply(_clean_cost)

    # Ensure online_order and book_table are clean strings
    for col in ("online_order", "book_table"):
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df.reset_index(drop=True, inplace=True)
    return df
