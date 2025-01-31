import re
import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__))+'/data'

def species_to_latex(sp):
    sp1 = re.sub(r'([0-9]+)', r"_\1", sp)
    sp1 = r'\mathrm{'+sp1+'}'
    if sp == 'O1D':
        sp1 = r'\mathrm{O(^1D)}'
    elif sp == 'N2D':
        sp1 = r'\mathrm{N(^2D)}'
    elif sp == '1CH2':
        sp1 = r'\mathrm{^1CH_2}'
    return sp1