import yaml
import pylatex as pl
import re

from .utils import species_to_latex, DATA_DIR

def reformat_equation(rx):
    rx1 = rx.replace('<=>','=>').replace('(','').replace(')','')
    tmp1 = [a.strip() for a in rx1.split('=>')[0].split('+')]
    tmp2 = [a.strip() for a in rx1.split('=>')[1].split('+')]
    tmp = (' + '.join(tmp1))+' => '+(' + '.join(tmp2))
    return tmp
    
def equation_to_latex(rx):
    rx1 = rx.replace('<=>','=>').replace('(','').replace(')','')
    tmp1 = [species_to_latex(a.strip()) for a in rx1.split('=>')[0].split('+')]
    tmp2 = [species_to_latex(a.strip()) for a in rx1.split('=>')[1].split('+')]
    tmp = '$'+(' + '.join(tmp1))+r' \rightarrow '+(' + '.join(tmp2))+'$'
    return tmp

def format_latex_scientific(number, precision=2):
    s = f"{number:.{precision}e}"  # Format as scientific notation
    mantissa, exponent = s.split("e")
    mantissa = remove_trailing_zeros(mantissa)
    exponent = int(exponent)
    if float(mantissa) == 1:
        return f"10^{{{exponent}}}"
    else:
        return f"{mantissa} \\times 10^{{{exponent}}}"

def remove_trailing_zeros(num_str):
    return num_str.rstrip('0').rstrip('.')

def latex_equation_from_rate(rate):
    if rate['A'] == 0:
        return '0'

    res = format_latex_scientific(rate['A'], 2)
    
    if rate['b'] != 0:
        res += ' T^{'+remove_trailing_zeros('%.2f'%rate['b'])+'}'
    
    if rate['Ea'] != 0:
        if rate['Ea'] < 0:
            tmp = ' e^{'+remove_trailing_zeros('%.2f'%(-rate['Ea']))+'/T}'
        else:
            tmp = ' e^{-'+remove_trailing_zeros('%.2f'%(rate['Ea']))+'/T}'
        res += tmp
    
    return res

def format_citation(ref):
    tmp = ref.replace(' ','').replace('rev-','')
    return r'\cite{'+tmp+'}'

def get_rxn_info():

    with open(DATA_DIR+'/reaction_mechanisms/zahnle_earth.yaml','r') as f:
        dat = yaml.load(f,yaml.Loader)
    
    reaction_info = []
    reactions = {}
    
    for j,rxn in enumerate(dat['reactions']):
        rx = rxn['equation']
        rx_type = 'elementary'
        if 'type' in rxn:
            rx_type = rxn['type']
            
        if rx_type == 'photolysis':
            continue

        reactions[reformat_equation(rx)] = j + 1
        
        eqn = equation_to_latex(rx)
        rate = None
        rate_high = None
        ref = None
        ref_high = None
    
        if rx_type in ['elementary','three-body']:
            rate = '$'+latex_equation_from_rate(rxn['rate-constant'])+'$'
            if 'ref' in rxn:
                ref = format_citation(rxn['ref'])
        elif rx_type in ['falloff']:
            rate = '$k_0 = '+latex_equation_from_rate(rxn['low-P-rate-constant'])+'$'
            rate_high = r'$k_\infty = '+latex_equation_from_rate(rxn['high-P-rate-constant'])+'$'
            if 'ref' in rxn:
                if 'low-P' in rxn['ref']:
                    ref = format_citation(rxn['ref']['low-P'])
                if 'high-P' in rxn['ref']:
                    ref_high = format_citation(rxn['ref']['high-P'])
        else:
            raise Exception(rx)
    
        res = {
            'equation': eqn,
            'type': rx_type,
            'rate': rate,
            'rate_high': rate_high,
            'ref': ref,
            'ref_high': ref_high
        }
        reaction_info.append(res)

    def replace_content(match):
        content = match.group(1)
        return r'R\ref{R'+str(reactions[reformat_equation(content)])+'}'
    pattern = re.escape(r'\ref{') + r"(.*?)" + re.escape('}')
    
    notes = []
    for note in dat['reaction-notes']:
        refs = [r'R\ref{R'+str(reactions[reformat_equation(a)])+'}' for a in note['reactions']]
        text = note['note']
        text = re.sub(pattern, replace_content, text)
        tmp = r'\noindent {\bf '+(', '.join(refs)) + ':} '+text
        notes.append(tmp)

    return reaction_info, notes

def build_reactions_table(nw=0.05, rxw=0.3, raw=0.3, cw=0.3):

    reaction_info, notes = get_rxn_info()

    rows = r"p{"+str(nw)+r"\textwidth} p{"+str(rxw)+r"\textwidth} p{"+str(raw)+r"\textwidth} p{"+str(cw)+r"\textwidth}"
    data_table = pl.LongTable(rows)
    
    data_table.add_hline()
    data_table.add_hline()
    data_table.add_row([r'#',"Reaction", "Rate", "Reference"])
    data_table.add_hline()
    data_table.end_table_header()
    
    for i,rx in enumerate(reaction_info):
        j = i + 1

        ref = rx['ref']
        if ref is None:
            ref = ''
        ref_high = rx['ref_high']
        if ref_high is None:
            ref_high = ''
    
        label = r'R\arabic{react}\refstepcounter{react}\label{R'+str(j+1)+r'}'
        row = [pl.NoEscape(label), pl.NoEscape(rx['equation']),pl.NoEscape(rx['rate']),pl.NoEscape(ref)]
        data_table.add_row(row)
    
        if reaction_info[i]['type'] in ['falloff']:
            row = ['', '',pl.NoEscape(rx['rate_high']),pl.NoEscape(ref_high)]
            data_table.add_row(row)
        
    data_table.add_hline()
    data_table.add_hline()

    return data_table, notes
