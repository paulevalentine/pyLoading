import pandas as pd
from IPython.core.display_functions import display


def calc_line_loads():
    unit_loads = pd.read_csv('../data/unit_loads.csv')
    display(unit_loads)
