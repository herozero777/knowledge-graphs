# refer to 
#   https://rdflib.readthedocs.io/en/stable/#getting-started
#   https://stackoverflow.com/questions/43524943/creating-rdf-file-using-csv-file-as-input
from rdflib import Graph, Literal, RDF, URIRef, FOAF, Namespace
import string
import pandas as pd
from os.path import join

OUTPUT_DIR = "data"
TEST_DATA = True

def make_str_url_friendly(url:str):
    url = url.replace("\'", "").replace("\"", "")
    for i in string.punctuation:
        url = url.replace(i, "_")
    url = url.replace(" ", "_")
    return url

if __name__ == '__main__':

    if TEST_DATA:
        df_author = pd.read_csv("data/processed/small/Author.csv")
        df_paper = pd.read_csv("data/processed/small/Paper.csv")
        df_author_link_paper = pd.read_csv("data/processed/small/writesA.csv")
        df_hasReview = pd.read_csv("data/processed/small/hasReview.csv")
        df_keyword = pd.read_csv("data/processed/small/Keyword.csv")
        df_hasKeyword = pd.read_csv("data/processed/small/hasKeyword.csv")

        df_venue = pd.read_csv("data/processed/small/Venue.csv")
        df_publication = pd.read_csv("data/processed/small/Publication.csv")
        df_hasArea = pd.read_csv("data/processed/small/hasArea.csv")
        df_submitPaper = pd.read_csv("data/processed/small/submitPaper.csv")
        df_publishPaper = pd.read_csv("data/processed/small/publishPaper.csv")
    else:
        df = pd.read_csv("data/raw/papers_data.csv")

    g = Graph()
    NS = Namespace("http://www.upc.abc/#")

    # Class IRIs
    AuthorTbox = URIRef("http://www.upc.abc/#Author")
    PaperTbox = URIRef("http://www.upc.abc/#Paper")
    FullPaperTbox = URIRef("http://www.upc.abc/#Full_Paper")
    ReviewTbox = URIRef("http://www.upc.abc/#Review")
    Area_KeyWordTBox = URIRef("http://www.upc.abc/#Area_KeyWord")

    VenueTbox = URIRef("http://www.upc.abc/#Venue")
    JournalTbox = URIRef("http://www.upc.abc/#Journal")
    ConferenceTbox = URIRef("http://www.upc.abc/#Conference")
    
    ChairTbox = URIRef("http://www.upc.abc/#Chair")
    EditorTbox = URIRef("http://www.upc.abc/#Editor")

    YearTbox = URIRef("http://www.upc.abc/#Year")
    PublicationTbox = URIRef("http://www.upc.abc/#Publication")
    CPTbox = URIRef("http://www.upc.abc/#Conference_Proceedings")
    JVTbox = URIRef("http://www.upc.abc/#Journal_Volume")

    # Properties IRIs
    hasReviewIRI = URIRef(NS + "hasReview")
    reviewerIRI = URIRef(NS + "reviewer")
    hasDecisionIRI = URIRef(NS + "hasDecision")
    hasTextIRI = URIRef(NS + "hasText")
    hasKeywordIRI = URIRef(NS + "hasKeyword")

    cHandledByIRI = URIRef(NS + "cHandledBy")
    jHandledByIRI = URIRef(NS + "jHandledBy")

    hasProceedingsIRI = URIRef(NS + "hasProceedings")
    hasVolumesIRI = URIRef(NS + "hasVolumes")

    submitPaperIRI = URIRef(NS + "submitTo")
    publishPaperIRI = URIRef(NS + "publishedIn")

    hasAreaIRI = URIRef(NS + "hasArea")
    hasYearIRI = URIRef(NS + "hasYear")

    # AssignedReviewerTbox = URIRef("http://www.upc.abc/#Assigned_Reviewer")

    ######################################################
    # Code Section
    ######################################################
    # Link author with paper
    df = pd.merge(df_author, df_author_link_paper, on="author_id" )
    df = pd.merge(df, df_paper, on="paper_id")
    for _, row in df.iterrows():

        author_name = make_str_url_friendly( row["author_name"] )
        paper_name = make_str_url_friendly( row["paper_title"] )

        # Define IRIs
        authorIRI = URIRef(AuthorTbox + "/" + author_name)
        authorNameIRI = URIRef(NS + "authorName")
        writesAIRI = URIRef(NS + "writesA")
        paperIRI = URIRef(FullPaperTbox + "/" + paper_name)

        # Define ABOXs, that is make TBOX-IRI as Class
        g.add((authorIRI, RDF.type, AuthorTbox))
        g.add((paperIRI, RDF.type, FullPaperTbox))

        # Connect instances of TBOX (ABOXes) via properties
        g.add((authorIRI, writesAIRI, paperIRI))
        g.add((authorIRI, authorNameIRI, Literal(author_name)))

    # link paper with review
    df = pd.merge(df_hasReview, df_paper, on='paper_id')
    df = pd.merge(df, df_author, left_on="reviewer_id", right_on='author_id')
    for _, row in df.iterrows():

        paper_name = make_str_url_friendly( row["paper_title"] )
        # Because authors are also reviewers
        reviewer_name = make_str_url_friendly( row["author_name"] )
        review_text = row["review_text"]
        decision = row["decision"]

        # Class IRIs
        # authorIRI = URIRef(AuthorTbox + "/" + author_name)
        paperIRI = URIRef(FullPaperTbox + "/" + paper_name)
        reviewIRI = URIRef(ReviewTbox + "/" + str(row["paper_id"]) + "-" + str(row["author_id"]))
        authorIRI = URIRef(AuthorTbox + "/" + reviewer_name)

        # Define ABOXs, that is make TBOX-IRI as Class
        g.add((reviewIRI, RDF.type, ReviewTbox))
        g.add((authorIRI, RDF.type, AuthorTbox))  # Should not be required in case of full data

        # Connect ABOXes (instances of TBOXes) via properties
        g.add((paperIRI, hasReviewIRI, reviewIRI))
        g.add((reviewIRI, reviewerIRI, authorIRI))
        g.add((reviewIRI, hasDecisionIRI, Literal(review_text) ))
        g.add((reviewIRI, hasTextIRI, Literal(decision) ))

    # link paper with keyword
    df = pd.merge(df_keyword, df_hasKeyword, on='keyword_id')
    df = pd.merge(df, df_paper, on='paper_id')
    for _, row in df.iterrows():

        paper_name = make_str_url_friendly(row["paper_title"])
        keyword = make_str_url_friendly(row["keyword_name"])
        # Class IRI
        areaIRI = URIRef(Area_KeyWordTBox + "/" + keyword)
        paperIRI = URIRef(FullPaperTbox + "/" + paper_name)

        # Connect instances of TBOX (ABOXes) via properties
        g.add((paperIRI, hasKeywordIRI, areaIRI))

    # link venue with area, handler
    df = pd.merge(df_keyword, df_hasArea, on='keyword_id')
    df = pd.merge(df, df_venue, on='venue_id')
    for _, row in df.iterrows():
        
        venue_name = make_str_url_friendly(row["venue_name"])
        keyword = make_str_url_friendly(row["keyword_name"])
        handler = make_str_url_friendly(row["handler"])

        areaIRI = URIRef(Area_KeyWordTBox + "/" + keyword)
        g.add((areaIRI, RDF.type, Area_KeyWordTBox))
        if row["venue_type"] == "Conference":
            veneuIRI = URIRef(ConferenceTbox + "/" + venue_name)
            g.add((veneuIRI, RDF.type, ConferenceTbox))
            handlerIRI = URIRef(ChairTbox + "/" + handler)
            g.add((handlerIRI, RDF.type, ChairTbox))
            g.add((veneuIRI, cHandledByIRI, handlerIRI))
        else:
            veneuIRI = URIRef(JournalTbox + "/" + venue_name)
            g.add((veneuIRI, RDF.type, JournalTbox))
            handlerIRI = URIRef(EditorTbox + "/" + handler)
            g.add((handlerIRI, RDF.type, EditorTbox))
            g.add((veneuIRI, jHandledByIRI, handlerIRI))

        g.add((veneuIRI, hasAreaIRI, areaIRI))

    # link publication with venue
    df = pd.merge(df_publication, df_venue, on='venue_id')
    for _, row in df.iterrows():

        publication_name = make_str_url_friendly(row["publication_name"])
        venue_name = make_str_url_friendly(row["venue_name"])
        publication_year = make_str_url_friendly(str(row["publication_year"]))

        # Class IRI
        if row["venue_type"] == "Conference":
            publicationIRI = URIRef(CPTbox + "/" + publication_name)
            g.add((publicationIRI, RDF.type, CPTbox))
            veneuIRI = URIRef(ConferenceTbox + "/" + venue_name)
            g.add((veneuIRI, hasProceedingsIRI, publicationIRI))
        else:
            publicationIRI = URIRef(JVTbox + "/" + publication_name)
            g.add((publicationIRI, RDF.type, JVTbox))
            veneuIRI = URIRef(JournalTbox + "/" + venue_name)
            g.add((veneuIRI, hasVolumesIRI, publicationIRI))
        yearIRI = URIRef(YearTbox + "/" + publication_year)
        g.add((yearIRI, RDF.type, YearTbox))
        g.add((publicationIRI, hasYearIRI, yearIRI))

    # link paper with venue, publication
    df = pd.merge(df_paper, df_publishPaper, on='paper_id')
    df = pd.merge(df, df_publication, on='publication_id')
    df = pd.merge(df, df_venue, on='venue_id')
    for _, row in df.iterrows():

        paper_name = make_str_url_friendly(row["paper_title"])
        publication_name = make_str_url_friendly(row["publication_name"])
        venue_name = make_str_url_friendly(row["venue_name"])
        
        veneuIRI = None
        publicationIRI = None
        if row["venue_type"] == "Conference":
            publicationIRI = URIRef(CPTbox + "/" + publication_name)
            veneuIRI = URIRef(ConferenceTbox + "/" + venue_name)
        else:
            publicationIRI = URIRef(JVTbox + "/" + publication_name)
            veneuIRI = URIRef(JournalTbox + "/" + venue_name)
        paperIRI = URIRef(FullPaperTbox + "/" + paper_name)

        g.add((paperIRI, submitPaperIRI, veneuIRI))
        g.add((paperIRI, publishPaperIRI, publicationIRI))

    print(" --- Completed Graph ---")
    print(f'file location: {join(OUTPUT_DIR, "test-auth-n-paper.nt")}')
    g.serialize( join(OUTPUT_DIR, "test-auth-n-paper.nt"), format='nt', encoding="utf-8")
    # Then import test-auth-n-paper.nt into GraphDB

# Depricated section

    # for index, row in df.iterrows():
    #
    #     author = make_str_url_friendly( row["Authors"] )
    #     paper = make_str_url_friendly( row["Paper"] )
    #
    #     # g.add((URIRef(Author + "/" + author), RDF.type, Author ))
    #     g.add((URIRef(Paper + "/" + paper), RDF.type, Paper ))
    #     # g.add((URIRef(Author + "/" + author), NS.name, Literal("Himanshu")))
    #
    #     g.add((URIRef(Author + "/" + author),  # Subject
    #             URIRef(NS + "writesA"),  # Predicate
    #             URIRef(Paper + "/" + paper) ))  # Object
    #
    #     g.add((URIRef(Author + "/" + author),
    #             URIRef(NS + "authorName"),
    #             Literal(author) ))
    #
    # g.serialize( join(OUTPUT_DIR, "test-auth-n-paper.nt"), format='nt', encoding="utf-8")
    #
    # # Then import test.nt into graphDB
