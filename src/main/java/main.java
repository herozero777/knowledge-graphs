//package jena.examples.rdf ;

import org.apache.jena.base.Sys;
import org.apache.jena.rdf.model.*;
import org.apache.jena.ontology.*;
import org.apache.jena.vocabulary.*;
import org.apache.jena.riot.*;

/** Tutorial 1 creating a simple model
 */

public class main {

    public static void createOntology() {
        // Name space for my model
        String NS = "http://www.upc.abc/#";

        // The OntModelSpec.RDFS_MEM_RDFS_INF: gives us rule reasoner with RDFS-level entailment-rules
        OntModel m = ModelFactory.createOntologyModel( OntModelSpec.RDFS_MEM_RDFS_INF );

        // Classes
        OntClass paper = m.createClass( NS + "Paper" );
        OntClass venue = m.createClass( NS + "Venue" );
        OntClass conference = m.createClass( NS + "Conference" );
        OntClass journal = m.createClass( NS + "Journal" );
        OntClass reviewer = m.createClass( NS + "Reviewer" );
        OntClass chair = m.createClass( NS + "Chair");
        OntClass editor = m.createClass(NS + "Editor");
        OntClass acceptOrReject = m.createClass(NS + "Accept-Or-Reject");
        OntClass reviewText = m.createClass(NS + "Review-Text");
        OntClass publications = m.createClass(NS + "Publications");
        OntClass conferenceProceedings = m.createClass(NS + "Conference-Proceedings");
        OntClass journalVolume = m.createClass(NS + "Journal-Volume");

        // Connecting Classes to sub-Classes
        venue.addSubClass( conference );
        venue.addSubClass( journal );

        publications.addSubClass( conferenceProceedings );
        publications.addSubClass( journalVolume );

        // Properties
        OntProperty submittedTo = m.createOntProperty(NS + "SubmitTo");
        OntProperty assignedReviewers = m.createOntProperty(NS + "AssignedReviewers");
        OntProperty cHandledBy = m.createOntProperty(NS + "Conf-Handled-By");
        OntProperty jHandledBy = m.createOntProperty(NS + "Jour-Handled-By");
        OntProperty decision = m.createOntProperty(NS + "Decision");
        OntProperty decisionText = m.createOntProperty(NS + "Decision-Text");
        OntProperty publishedIn = m.createOntProperty(NS + "Published-In");

        // Connecting properties to classes
        submittedTo.addDomain( paper );
        submittedTo.addRange( venue );
        submittedTo.addLabel("Paper is submitted to venue", "en");

        assignedReviewers.addDomain( paper );
        assignedReviewers.addRange( reviewer );

        cHandledBy.addDomain( conference );
        cHandledBy.addRange( chair );

        jHandledBy.addDomain( journal );
        jHandledBy.addRange( editor );

        decision.addDomain( paper );
        decision.addRange( acceptOrReject );

        decisionText.addDomain( acceptOrReject );
        decisionText.addRange( reviewText );

        publishedIn.addDomain( paper );
        publishedIn.addRange( publications );

        // Write the model in XML format to the std-out
        m.write(System.out);
    }

    public static void main (String args[]) {

        // some definitions
        String personURI    = "http://somewhere/JohnSmith/#";
        String givenName    = "John";
        String familyName   = "Smith";
        String fullName     = givenName + " " + familyName;

        // create an empty model
        Model model = ModelFactory.createDefaultModel();

        // create the resource
        //   and add the properties cascading style
        Resource johnSmith
                = model.createResource(personURI)
                .addProperty(VCARD.FN, fullName)
                .addProperty(VCARD.N,
                        model.createResource()
                                .addProperty(VCARD.Given, givenName)
                                .addProperty(VCARD.Family, familyName));

        // list the statements in the graph
        StmtIterator iter = model.listStatements();

        // print out the predicate, subject and object of each statement
        while (iter.hasNext()) {
            Statement stmt      = iter.nextStatement();         // get next statement
            Resource  subject   = stmt.getSubject();   // get the subject
            Property  predicate = stmt.getPredicate(); // get the predicate
            RDFNode   object    = stmt.getObject();    // get the object

            System.out.print(subject.toString());
            System.out.print(" " + predicate.toString() + " ");
            if (object instanceof Resource) {
                System.out.print(object.toString());
            } else {
                // object is a literal
                System.out.print(" \"" + object.toString() + "\"");
            }
            System.out.println(" .");
        }

        // now write the model in XML form to a file
        model.write( System.out);
        // now write the model in a pretty form
//        RDFDataMgr.write(System.out, model, Lang.RDFXML);

    }
}

