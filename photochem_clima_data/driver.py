import pylatex as pl
import requests
import shutil
from .xsections import build_xsections_table
from .reactions import build_reactions_table
from .utils import DATA_DIR

def download_aastex():
    url = "https://journals.aas.org/wp-content/uploads/2021/02/aastex631.cls"
    response = requests.get(url, headers={'User-Agent': '...'})
    if response.status_code != 200:
        raise Exception("Failed to Download AASTeX")
    with open('aastex631.cls','w') as f:
        f.write(response.content.decode())

    url = 'https://journals.aas.org/wp-content/uploads/2019/06/aasjournal.bst'
    response = requests.get(url, headers={'User-Agent': '...'})
    if response.status_code != 200:
        raise Exception("Failed to Download AASTeX")
    with open('aasjournal.bst','w') as f:
        f.write(response.content.decode())

    shutil.copyfile(DATA_DIR+'/bib.bib', './bib.bib')

def make_document(filename='photochemclimadata'):

    download_aastex()
    
    doc = pl.Document(documentclass='aastex631')

    # Packages
    doc.preamble.append(pl.Package('multirow'))
    
    # Counters
    doc.preamble.append(pl.Command('newcounter',arguments='photo'))
    doc.preamble.append(pl.Command('newcounter',arguments='react'))

    # Content
    doc.append(pl.NoEscape(r'\refstepcounter{photo}\label{P1}'))
    doc.append(build_xsections_table())
    data_table, notes = build_reactions_table()
    doc.append(pl.NoEscape(r'\refstepcounter{react}\label{R1}'))
    doc.append(data_table)
    with doc.create(pl.Section("Reaction Notes")):
        for note in notes:
            doc.append(pl.NoEscape(note+r'\newline'))
    
    # Bibliography
    doc.append(pl.Command('bibliography',arguments=pl.NoEscape('bib')))
    doc.append(pl.Command('bibliographystyle',arguments='aasjournal'))

    # Save
    doc.generate_pdf(filename, clean_tex=False)