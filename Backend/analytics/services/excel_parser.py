import pandas as pd

#    Ensure column names are unique and clean
def _make_unique_columns(cols):
    seen = {}
    unique = []
    for c in cols:
        base = str(c).strip()
        if base == "" or base.lower() == "nan":
            base = "Unnamed"
        if base not in seen:
            seen[base] = 1
            unique.append(base)
        else:
            seen[base] += 1
            unique.append(f"{base}_{seen[base]}")
    return unique


def parse_excel_second_row_headers(file_path: str) -> pd.DataFrame:
    df_raw = pd.read_excel(file_path, header=None)

    if df_raw.shape[0] < 3:
        raise ValueError("Excel file must contain at least 3 rows (metadata, header, data).")

    headers = df_raw.iloc[1].tolist() 
    headers = _make_unique_columns(headers)

    df = df_raw.iloc[2:].copy()   
    df.columns = headers

    df.dropna(how="all", inplace=True)

    df = df.where(pd.notnull(df), None)

    df.reset_index(drop=True, inplace=True)
    return df