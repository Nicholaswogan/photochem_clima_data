import pylatex as pl
from .xsections import build_xsections_table
from .utils import DATA_DIR

def add_preamble(doc):
    
    # Packages
    doc.preamble.append(pl.Package('natbib'))
    doc.preamble.append(pl.Package(pl.NoEscape(DATA_DIR+'/aasmacros')))
    doc.preamble.append(pl.Package('multirow'))
    doc.preamble.append(pl.Package('hyperref',options='hidelinks'))

    # Counters
    doc.preamble.append(pl.Command('newcounter',arguments='photo'))

def make_document(filename='photochemclimadata', doc=None):
    if doc is None:
        doc = pl.Document(page_numbers=True, geometry_options={"margin": "1in"})
    
    # Preamble
    add_preamble(doc)

    # Xsections
    doc.append(build_xsections_table())
    
    # Bibliography
    doc.append(pl.Command('bibliography',arguments=pl.NoEscape(DATA_DIR+'/bib')))
    doc.append(pl.Command('bibliographystyle',arguments='plainnat'))

    # Save
    doc.generate_pdf(filename, clean_tex=False)