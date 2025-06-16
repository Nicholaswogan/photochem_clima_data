import pylatex as pl
import os
import h5py
from collections import Counter
import string
import yaml

from .utils import species_to_latex, DATA_DIR

def get_photo_species_and_reactions():

    filenames = [a for a in os.listdir(DATA_DIR+'/xsections/') if '.h5' in a and a != 'bins.h5']
    species = []
    reactions = []
    for filename in filenames:
        sp = filename.strip('.h5')
        species.append(sp)
        branches = []
        with h5py.File(DATA_DIR+'/xsections/'+filename,'r') as f:
            try:
                branches = [a for a in list(f['photodissociation-qy'].keys()) if a != 'wavelengths']
            except KeyError:
                pass
        for b in branches:
            reactions.append(b)

    return species, reactions
    
def get_citation_abrv(dat, species):
    citations = []
    for sp in species:
        cits = [b for a in dat[sp]['xsections'] for b in a['citations']]
        if 'photodissociation-qy' in dat[sp]:
            cits += [b for a in dat[sp]['photodissociation-qy'] for b in a['citations']]
        for c in cits:
            citations.append(c)
    citations = [a for a in citations if a != 'Assumed']
    citations_counts = dict(Counter(citations))
    citations_counts = {k: v for k, v in sorted(citations_counts.items(), key=lambda item: item[1], reverse=True)}
    i = 0
    alphabet = list(string.ascii_lowercase)
    citation_abrv = {}
    for key in citations_counts:
        if citations_counts[key] > 2:
            citation_abrv[key] = alphabet[i]
            i+=1

    return citation_abrv

def process_citations(cits, citation_abrv):
    tmp1 = []
    tmp2 = []
    for cits1 in cits:
        for a in cits1['citations']:
            if a in citation_abrv:
                tmp1.append(citation_abrv[a])
            elif a == 'Assumed':
                tmp1.append(a)
            else:
                tmp2.append(a)

    tmp1 = list(set(tmp1))
    tmp2 = list(set(tmp2))
    val = ''
    if len(tmp1) > 0:
        val += ', '.join(tmp1)
    if len(tmp2) > 0:
        if len(val) > 0:
            val += ', '
        val += r'\cite{'+','.join(tmp2)+'}'
    return val

def get_citations(dat, species, citation_abrv):
    citations_xs = {}
    citations_qy = {}
    sp_to_notes = {}
    for sp in species:
        xs = dat[sp]['xsections']
        val = process_citations(xs, citation_abrv)
        citations_xs[sp] = val
        if 'notes' in dat[sp]:
            sp_to_notes[sp] = dat[sp]['notes']
        if 'photodissociation-qy' in dat[sp]:
            qy = dat[sp]['photodissociation-qy']
            citations_qy[sp] = process_citations(qy, citation_abrv)
    return citations_xs, citations_qy, sp_to_notes

def get_sp_to_react(species, reactions):
    sp_to_react = {}
    for sp in species:
        sp_to_react[sp] = []
        for rx in reactions:
            sp1 = rx.split('+')[0].strip()
            if sp == sp1:
                tmp = [species_to_latex(a.strip()) for a in rx.split('=>')[1].split('+')]
                tmp = r'$\rightarrow '+(' + '.join(tmp))+'$'
                sp_to_react[sp].append(tmp)
    return sp_to_react

def get_xsections_info():

    # Load metadata
    with open(DATA_DIR+'/xsections/metadata.yaml','r') as f:
        dat = yaml.load(f,yaml.Loader)
    
    # Get species and reactions
    species, reactions = get_photo_species_and_reactions()

    # Get reactions associated with each species
    sp_to_react = get_sp_to_react(species, reactions)

    # Sort species alphabetically
    species.sort()

    # Get citations
    citation_abrv = get_citation_abrv(dat, species)
    citations_xs, citations_qy, sp_to_notes = get_citations(dat, species, citation_abrv)

    return species, sp_to_react, citation_abrv, citations_xs, citations_qy, sp_to_notes

def build_xsections_table(nw=0.05, spw=0.1, rxw=0.2, xsw=0.29, qyw=0.29, notew=0.93):
    species, sp_to_react, citation_abrv, citations_xs, citations_qy, sp_to_notes = get_xsections_info()

    rows = r"p{"+str(nw)+r"\textwidth} p{"+str(spw)+r"\textwidth} p{"+str(rxw)+r"\textwidth} p{"+str(xsw)+r"\textwidth} p{"+str(qyw)+r"\textwidth}"
    data_table = pl.LongTable(rows)

    data_table.add_hline()
    data_table.add_hline()
    data_table.add_row([r'#',"Species", "Reactions", "Cross Section Ref.", 'Yield Ref.'])
    data_table.add_hline()
    data_table.end_table_header()

    num_to_notes = {}
    j = 1
    for i,sp in enumerate(species):
        rxs = sp_to_react[sp]
        sp_latex = '$'+species_to_latex(sp)+'$'
        if sp in sp_to_notes:
            num_to_notes[j] = sp_to_notes[sp]

        if len(rxs) == 0:
            label = r'\refstepcounter{photo}\label{P'+str(j)+r'}P\arabic{photo}'
            row = [pl.NoEscape(label), pl.NoEscape(sp_latex), '-',pl.NoEscape(citations_xs[sp]),'-']
            data_table.add_row(row)
            j += 1
        elif len(rxs) == 1:
            label = r'\refstepcounter{photo}\label{P'+str(j)+r'}P\arabic{photo}'
            row = [pl.NoEscape(label), pl.NoEscape(sp_latex), pl.NoEscape(rxs[0]),pl.NoEscape(citations_xs[sp]),pl.NoEscape(citations_qy[sp])]
            data_table.add_row(row)
            j += 1
        else:
            label = r'\refstepcounter{photo}\label{P'+str(j)+r'}P\arabic{photo}'
            row = [
                pl.NoEscape(label), 
                pl.NoEscape(sp_latex), 
                pl.NoEscape(rxs[0]),
                pl.NoEscape(r'\multirow[t]{'+str(len(rxs))+'}{'+str(xsw)+r'\textwidth'+'}{'+citations_xs[sp]+'}'),
                pl.NoEscape(r'\multirow[t]{'+str(len(rxs))+'}{'+str(qyw)+r'\textwidth'+'}{'+citations_qy[sp]+'}')
            ]
            data_table.add_row(row)
            j += 1
            for i,rx in enumerate(rxs[1:]):
                label = r'\refstepcounter{photo}\label{P'+str(j)+r'}P\arabic{photo}'
                row = [
                    pl.NoEscape(label),
                    '', 
                    pl.NoEscape(rx),
                    '',
                    ''
                ]
                data_table.add_row(row)
                j += 1
    data_table.add_hline()
    data_table.add_hline()

    tmp = r'\textbf{Notes.} '
    for cit in citation_abrv:
        val = citation_abrv[cit]
        tmp += val+r': \cite{'+cit+'}; '
    tmp = tmp[:-2]+'.'
    for key in num_to_notes:
        tmp += r' P\ref{P'+str(key)+r'}: '+num_to_notes[key]

    row = [pl.MultiColumn(5, align=pl.NoEscape(r"p{"+str(notew)+r"\textwidth}"), data=pl.NoEscape(tmp))]
    data_table.add_row(row)

    return data_table