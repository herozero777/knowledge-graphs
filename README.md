# SDM Lab 3

context of our graph:


### Questions/ Queries
#### Context:
- Link: https://jena.apache.org/documentation/ontology/#instances-or-individuals
- heading on the page: Ontology languages and the Jena Ontology API
- 6th paragraph is:
The predicate names defined in the ontology language correspond to the accessor methods on the Java classes in the API. For example, an OntClass has a method to list its super-classes, which corresponds to the values of the subClassOf property in the RDF representation. This point is worth re-emphasising: no information is stored in the OntClass object itself. When you call the OntClass listSuperClasses() method, Jena will retrieve the information from the underlying RDF triples. Similarly, adding a subclass to an OntClass asserts an additional RDF triple, typically with predicate rdfs:subClassOf into the model.

What does the above mean?

Q 2):
It is okay to use same property name in TBOXes. E.g. Conference_Proceedings will have an year and Journal_Volume will have an year. So can I go like for both "hasYear" property? 
I'm asking because I vaguely remember maybe professor said that not to do this.

## Notes on Knowledge Graphs

### SPARQL 
`a` can be used as a predicate to mean `http://www.w3.org/1999/02/22-rdf-syntax-ns#type`, 
which we also know as `rdf:type`

## Query keywords
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT DISTINCT ?a ?b WHERE 
{ 
    ?paper a NS:Paper .
    ?paper NS:HasKeyword ?area_keyword .
    ?area_keyword NS:keyname "ML"
    
} LIMIT 50

### Resources:
To understand Java Jena API:
https://jena.apache.org/tutorials/rdf_api.html

To understand Jena Ontology API:
https://jena.apache.org/documentation/ontology/#instances-or-individuals

#### For Python refer to 
https://rdflib.readthedocs.io/en/stable/#getting-started
https://stackoverflow.com/questions/43524943/creating-rdf-file-using-csv-file-as-input
