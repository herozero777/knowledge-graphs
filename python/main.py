# refer to 
#   https://rdflib.readthedocs.io/en/stable/#getting-started
#   https://stackoverflow.com/questions/43524943/creating-rdf-file-using-csv-file-as-input
from rdflib import Graph, Literal, RDF, URIRef, FOAF, Namespace
import string
import pandas as pd
from os.path import join

OUTPUT_DIR = "data"

df = pd.read_csv("data/raw/papers_data.csv")
print(df)

g = Graph()
NS = Namespace("http://www.upc.abc/#")

Author = URIRef("http://www.upc.abc/#Author")
Paper = URIRef("http://www.upc.abc/#Full_Paper")

conf = Namespace("http://bdma.upc.abc/conference/")
schema = Namespace('http://schema.bdma.upc.abc/')

def make_str_url_friendly(url:str):
    url = url.replace("\'", "").replace("\"", "")
    for i in string.punctuation:
        url = url.replace(i, "_")
    url = url.replace(" ", "_")
    return url


for index, row in df.iterrows():

    author = make_str_url_friendly( row["Authors"] )
    paper = make_str_url_friendly( row["Paper"] )

    g.add((URIRef(Author + "/" + author), RDF.type, Author ))
    g.add((URIRef(Paper + "/" + paper), RDF.type, Paper ))

    g.add((URIRef(Author + "/" + author),  # Subject
            URIRef(NS + "Writes-A"),  # Predicate
            URIRef(Paper + "/" + paper)))  # Object

g.serialize( join(OUTPUT_DIR, "test-auth-n-paper.nt"), format='nt', encoding="utf-8")

# Then import test.nt into graphDB
