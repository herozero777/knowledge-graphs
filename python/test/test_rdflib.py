# refer to 
#   https://rdflib.readthedocs.io/en/stable/#getting-started
#   https://stackoverflow.com/questions/43524943/creating-rdf-file-using-csv-file-as-input
from rdflib import Graph, Literal, RDF, URIRef, FOAF, Namespace
import csv
import pandas as pd

pd_reader = pd.read_csv("./test_data.csv")
print(pd_reader)

g = Graph()
ppl = Namespace("http://bdma.upc.abc/person/")
ppr = Namespace("http://bdma.upc.abc/paper/")
conf = Namespace("http://bdma.upc.abc/conference/")
schema = Namespace('http://schema.bdma.upc.abc/')

for index, row in pd_reader.iterrows():
    g.add((URIRef(ppl+row["Author"]), RDF.type, FOAF.Person))
    g.add((URIRef(ppl+row["Reviewer1"]), RDF.type, FOAF.Person))
    g.add((URIRef(ppl+row["Reviewer2"]), RDF.type, FOAF.Person))

    g.add((URIRef(ppr+row["Paper"]), URIRef(schema+"wroteBy"), URIRef(ppl+row["Author"])))
    g.add((URIRef(ppr+row["Paper"]), URIRef(schema+"publishedIn"), URIRef(conf+row["Conference"])))
    g.add((URIRef(ppr+row["Paper"]), URIRef(schema+"reviewedBy"), URIRef(ppl+row["Reviewer1"])))
    g.add((URIRef(ppr+row["Paper"]), URIRef(schema+"reviewedBy"), URIRef(ppl+row["Reviewer2"])))
    
g.serialize('test.nt',format='nt')

# Then import test.nt into graphDB