import pandas as pd
from pathlib import Path

from IPython.core.display_functions import display
# Set display options to avoid the multi-line wrapping bug in Python 3.14
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)

def calc_line_loads():
    unit_loads = pd.read_csv('./unit_loads.csv', index_col=0)
    print("Unit permanent loads (kN/m^2):")
    unit_loads=unit_loads.iloc[:,:-1]
    unit_loads['Total gk'] = unit_loads.sum(axis=1)
    unit_loads.to_csv('./unit_loads.csv')
    display(unit_loads)

    variable_file = Path('./variable_loads.csv')
    if variable_file.exists():
        variable_loads = pd.read_csv('./variable_loads.csv', index_col=0)
        if variable_loads.index.tolist() != unit_loads.index.tolist():
            print("Error : Variable load categories do not match dead load data")
            display(variable_loads.head())
            return 0
    else:
        variable_loads = pd.DataFrame(index=unit_loads.index, columns=['qk'])
        variable_loads.to_csv('./variable_loads.csv')

    print("Unit variable loads (kN/m^2):")
    display(variable_loads)

    line_file = Path('./load_lines.csv')
    if line_file.exists():
        load_lines = pd.read_csv('./load_lines.csv', index_col=0)
        if load_lines.columns.tolist() != unit_loads.index.tolist():
            print("Error : line load load categories do no math span data")
            display(load_lines.head())
            return 0
    else:
        load_lines = pd.DataFrame(columns=unit_loads.index)
        load_lines.to_csv('./load_lines.csv')

    print("Supported lengths (m):")
    display(load_lines)

    load_lines_transposed = load_lines.transpose()
    names = load_lines_transposed.columns.tolist()
    load_summary  = pd.DataFrame(index=names)
    detailed_loads = pd.DataFrame(index = unit_loads.index)
    detailed_variable_loads = pd.DataFrame(index = unit_loads.index)
    for name in names:
        detailed_loads[name] = load_lines_transposed[name] * unit_loads['Total gk']
        detailed_variable_loads[name] = load_lines_transposed[name] * variable_loads['qk']

    print("Permanent load composition (kN/m):")
    detailed_loads.loc['Total Gk', detailed_loads.columns] = detailed_loads[detailed_loads.columns].sum()
    display(detailed_loads)

    print("Variable load composition (kN/m):")
    detailed_variable_loads.loc['Total Qk', detailed_variable_loads.columns] = detailed_variable_loads[detailed_variable_loads.columns].sum()
    display(detailed_variable_loads)

    load_summary['Gk'] = detailed_loads.loc['Total Gk',:]
    load_summary['Qk'] = detailed_variable_loads.loc['Total Qk',:]
    print("Load summary (kN/m):")
    display(load_summary)

    return load_summary
