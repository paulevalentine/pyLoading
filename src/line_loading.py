import pandas as pd
from pathlib import Path

from IPython.core.display_functions import display
# Set display options to avoid the multi-line wrapping bug in Python 3.14
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)

def calc_line_loads():
    unit_loads = pd.read_csv('../data/unit_loads.csv', index_col=0)
    print("Unit permanent loads (kN/m^2):")
    unit_loads=unit_loads.iloc[:,:-1]
    unit_loads['Total Gk'] = unit_loads.sum(axis=1)
    unit_loads.to_csv('../data/unit_loads.csv')
    display(unit_loads)


    line_file = Path('../data/load_lines.csv')
    if line_file.exists():
        load_lines = pd.read_csv('../data/load_lines.csv', index_col=0)
        if load_lines.columns.tolist() != unit_loads.index.tolist():
            print("Error : line load load categories do no math span data")
            display(load_lines.head())
    else:
        load_lines = pd.DataFrame(columns=unit_loads.index)
        load_lines.to_csv('../data/load_lines.csv')

    print("Supported lengths (m):")
    display(load_lines)

    return unit_loads
