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
    else:
        df = pd.read_csv("data/raw/papers_data.csv")

    g = Graph()
    NS = Namespace("http://www.upc.abc/#")

    # Class IRIs
    AuthorTbox = URIRef("http://www.upc.abc/#Author")
    PaperTbox = URIRef("http://www.upc.abc/#Paper")
    FullPaperTbox = URIRef("http://www.upc.abc/#Full_Paper")
    ReviewTbox = URIRef("http://www.upc.abc/#Review")
    # Properties IRIs
    hasReviewIRI = URIRef(NS + "hasReview")
    reviewerIRI = URIRef(NS + "reviewer")
    hasDecisionIRI = URIRef(NS + "hasDecision")
    hasTextIRI = URIRef(NS + "hasText")

    # AssignedReviewerTbox = URIRef("http://www.upc.abc/#Assigned_Reviewer")

    conf = Namespace("http://bdma.upc.abc/conference/")
    schema = Namespace('http://schema.bdma.upc.abc/')

    ######################################################
    # Code Section
    ######################################################
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

        # Connect instances of TBOX (ABOXes) via properties
        g.add((paperIRI, hasReviewIRI, reviewIRI))
        g.add((reviewIRI, reviewerIRI, authorIRI))
        g.add((reviewIRI, hasDecisionIRI, Literal(review_text) ))
        g.add((reviewIRI, hasTextIRI, Literal(decision) ))

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
