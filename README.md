# SDM Lab 3

### Queries
#### Context:
- Link: https://jena.apache.org/documentation/ontology/#instances-or-individuals
- heading on the page: Ontology languages and the Jena Ontology API
- 6th paragraph is:
The predicate names defined in the ontology language correspond to the accessor methods on the Java classes in the API. For example, an OntClass has a method to list its super-classes, which corresponds to the values of the subClassOf property in the RDF representation. This point is worth re-emphasising: no information is stored in the OntClass object itself. When you call the OntClass listSuperClasses() method, Jena will retrieve the information from the underlying RDF triples. Similarly, adding a subclass to an OntClass asserts an additional RDF triple, typically with predicate rdfs:subClassOf into the model.

What does the above mean?


### Resources:
To understand Java Jena API:
https://jena.apache.org/tutorials/rdf_api.html

To understand Jena Ontology API:
https://jena.apache.org/documentation/ontology/#instances-or-individuals

#### For Python refer to 
https://rdflib.readthedocs.io/en/stable/#getting-started
https://stackoverflow.com/questions/43524943/creating-rdf-file-using-csv-file-as-input
