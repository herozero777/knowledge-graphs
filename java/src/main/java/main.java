//package jena.examples.rdf ;

import org.apache.jena.base.Sys;
import org.apache.jena.rdf.model.*;
import org.apache.jena.ontology.*;
import org.apache.jena.vocabulary.*;
import org.apache.jena.riot.*;

import static org.apache.jena.vocabulary.RDFSyntax.literal;

/** Tutorial 1 creating a simple model
 */

public class main {

    public static void createOntology() {
        // Name space for my model
        String NS = "http://www.upc.abc/#";

        // The OntModelSpec.RDFS_MEM_RDFS_INF: gives us rule reasoner with RDFS-level entailment-rules
        OntModel m = ModelFactory.createOntologyModel( OntModelSpec.RDFS_MEM_RDFS_INF );

        // Classes
        OntClass full_paper = m.createClass( NS + "Full_Paper" );
        OntClass short_paper = m.createClass( NS + "Short_Paper" );
        OntClass demo_paper = m.createClass( NS + "Demo_Paper");
        OntClass poster = m.createClass( NS + "Poster" );
        OntClass paper = m.createClass( NS + "Paper" );

        OntClass author = m.createClass( NS + "Author" );
        OntClass venue = m.createClass( NS + "Venue" );
        OntClass conference = m.createClass( NS + "Conference" );
        OntClass journal = m.createClass( NS + "Journal" );
        OntClass chair = m.createClass( NS + "Chair");
        OntClass editor = m.createClass(NS + "Editor");
        OntClass publication = m.createClass(NS + "Publication");
        OntClass conferenceProceedings = m.createClass(NS + "Conference_Proceedings");
        OntClass journalVolume = m.createClass(NS + "Journal_Volume");

        OntClass area_keyword = m.createClass( NS + "Area_KeyWord");
        OntClass review = m.createClass(NS + "Review");
        OntClass year = m.createClass(NS + "Year");

        // Connecting Classes to sub-Classes
        paper.addSubClass( poster );
        paper.addSubClass( demo_paper );
        paper.addSubClass( short_paper );
        paper.addSubClass( full_paper );
        venue.addSubClass( conference );
        venue.addSubClass( journal );

        publication.addSubClass( conferenceProceedings );
        publication.addSubClass( journalVolume );

        // Properties
        OntProperty writesA = m.createOntProperty(NS + "writesA");
        OntProperty authorName = m.createOntProperty(NS + "authorName");
        OntProperty hasKeyword = m.createOntProperty(NS + "hasKeyword");
        OntProperty submittedTo = m.createOntProperty(NS + "submitTo");
        OntProperty cHandledBy = m.createOntProperty(NS + "cHandledBy");
        OntProperty jHandledBy = m.createOntProperty(NS + "jHandledBy");
        OntProperty hasReview = m.createOntProperty(NS + "hasReview");
        OntProperty reviewer = m.createOntProperty(NS + "reviewer");
        OntProperty hasDecision = m.createOntProperty(NS + "hasDecision");
        OntProperty hasText = m.createOntProperty(NS + "hasText");
        OntProperty publishedIn = m.createOntProperty(NS + "publishedIn");
        OntProperty ofArea = m.createOntProperty(NS + "ofArea");
        OntProperty hasVolume = m.createOntProperty(NS + "hasVolume");
        OntProperty hasProceedings = m.createOntProperty(NS + "hasProceedings");
        OntProperty jHasYears = m.createOntProperty(NS + "jHasYears");
        OntProperty cHasYears = m.createOntProperty(NS + "cHasYears");

        // Connecting properties to classes
        authorName.addDomain( author );
        authorName.addRange( RDFS.Literal );
        writesA.addDomain( author );
        writesA.addRange( paper );
        hasKeyword.addDomain( paper );
        hasKeyword.addRange( area_keyword );
        ofArea.addDomain( venue );
        ofArea.addRange( area_keyword );
        submittedTo.addDomain( paper );
        submittedTo.addRange( venue );
        submittedTo.addLabel("Paper is submitted to venue", "en");

        hasReview.addDomain( paper );
        hasReview.addRange( review );

        cHandledBy.addDomain( conference );
        cHandledBy.addRange( chair );
        hasProceedings.addDomain( conference );
        hasProceedings.addRange( conferenceProceedings );
        cHasYears.addDomain( conferenceProceedings );
        cHasYears.addRange( year );
        jHandledBy.addDomain( journal );
        jHandledBy.addRange( editor );
        hasVolume.addDomain( journal );
        hasVolume.addRange( journalVolume );
        jHasYears.addDomain( journalVolume );
        jHasYears.addRange( year );

        reviewer.addDomain( review );
        reviewer.addRange( author );

        hasDecision.addDomain( review );
        hasDecision.addRange( RDFS.Literal );

        hasText.addDomain( review );
        hasText.addRange( RDFS.Literal );

        publishedIn.addDomain( paper );
        publishedIn.addRange( publication );

        // Write the model in XML format to the std-out
        m.write(System.out);
    }

    public static void main (String args[]) {
//
        createOntology();
//        // some definitions
//        String personURI    = "http://somewhere/JohnSmith/#";
//        String givenName    = "John";
//        String familyName   = "Smith";
//        String fullName     = givenName + " " + familyName;
//
//        // create an empty model
//        Model model = ModelFactory.createDefaultModel();
//
//        // create the resource
//        //   and add the properties cascading style
//        Resource johnSmith
//                = model.createResource(personURI)
//                .addProperty(VCARD.FN, fullName)
//                .addProperty(VCARD.N,
//                        model.createResource()
//                                .addProperty(VCARD.Given, givenName)
//                                .addProperty(VCARD.Family, familyName));
//
//        // list the statements in the graph
//        StmtIterator iter = model.listStatements();
//
//        // print out the predicate, subject and object of each statement
//        while (iter.hasNext()) {
//            Statement stmt      = iter.nextStatement();         // get next statement
//            Resource  subject   = stmt.getSubject();   // get the subject
//            Property  predicate = stmt.getPredicate(); // get the predicate
//            RDFNode   object    = stmt.getObject();    // get the object
//
//            System.out.print(subject.toString());
//            System.out.print(" " + predicate.toString() + " ");
//            if (object instanceof Resource) {
//                System.out.print(object.toString());
//            } else {
//                // object is a literal
//                System.out.print(" \"" + object.toString() + "\"");
//            }
//            System.out.println(" .");
//        }
//
//        // now write the model in XML form to a file
//        model.write( System.out);
//        // now write the model in a pretty form
////        RDFDataMgr.write(System.out, model, Lang.RDFXML);

    }
}

