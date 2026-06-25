import pandas as pd
from pathlib import Path

from IPython.core.display_functions import display
# Set display options to avoid the multi-line wrapping bug in Python 3.14
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)

# Input files (read-only to this module). Categories are the row index of the
# unit-load tables and the column headers of the supported-length table.
UNIT_LOADS_FILE = Path('./unit_loads.csv')
VARIABLE_LOADS_FILE = Path('./variable_loads.csv')
LOAD_LINES_FILE = Path('./load_lines.csv')


def _read_csv(path):
    """Read an input CSV, indexed by its first column, or raise a clear error.

    Inputs are treated as read-only: a missing file stops the calculation
    rather than silently seeding blank data."""
    if not path.exists():
        raise FileNotFoundError(
            f"Required loading input '{path}' not found. "
            f"Create it before running the calculation."
        )
    df = pd.read_csv(path, index_col=0)
    df.columns = df.columns.str.strip()
    return df


def calc_line_loads():
    # --- Unit permanent loads ------------------------------------------------
    # Read only the component columns; 'Total gk' is a derived output and is
    # recomputed every run, never read back from (or written to) the file.
    unit_loads = _read_csv(UNIT_LOADS_FILE)
    unit_loads = unit_loads.drop(columns='Total gk', errors='ignore')
    unit_loads['Total gk'] = unit_loads.sum(axis=1)
    categories = unit_loads.index

    print("Unit permanent loads (kN/m^2):")
    display(unit_loads)

    # --- Unit variable loads -------------------------------------------------
    variable_loads = _read_csv(VARIABLE_LOADS_FILE)
    if list(variable_loads.index) != list(categories):
        raise ValueError(
            "Variable load categories do not match permanent load categories.\n"
            f"  permanent: {list(categories)}\n"
            f"  variable:  {list(variable_loads.index)}"
        )
    print("Unit variable loads (kN/m^2):")
    display(variable_loads)

    # --- Supported lengths ---------------------------------------------------
    load_lines = _read_csv(LOAD_LINES_FILE)
    if list(load_lines.columns) != list(categories):
        raise ValueError(
            "Supported-length categories do not match unit-load categories.\n"
            f"  unit loads:        {list(categories)}\n"
            f"  supported lengths: {list(load_lines.columns)}"
        )
    print("Supported lengths (m):")
    display(load_lines)

    # --- Line loads ----------------------------------------------------------
    # The line load on each element is the supported-length matrix times the
    # unit-load vector. Stacking gk and qk into one [categories x 2] matrix
    # yields both actions from a single label-aligned matrix multiply.
    unit = pd.DataFrame({
        'Gk': unit_loads['Total gk'],
        'Qk': variable_loads['qk'],
    })
    load_summary = load_lines.dot(unit)

    # Per-category composition (kept for traceability): the unsummed
    # contribution of each load category to every element.
    print("Permanent load composition (kN/m):")
    display(load_lines.mul(unit_loads['Total gk'], axis=1))

    print("Variable load composition (kN/m):")
    display(load_lines.mul(variable_loads['qk'], axis=1))

    print("Load summary (kN/m):")
    display(load_summary)

    return load_summary
