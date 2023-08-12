import os
import rdflib
from rdflib import Graph, Namespace, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD, OWL, RDF, RDFS

import xml.etree.ElementTree as ET

owl_graph = Graph()
ns = Namespace("http://www.semanticweb.org/hrishi/ontologies/2023/4/untitled-ontology-10#")

# Parsing XML from the file moviesCatalog.xml

tree = ET.parse('moviesCatalog.xml')
root = tree.getroot()

# extend OWL ontology with local xml prefixes

owl_graph.bind('xml', 'http://www.w3.org/XML/2000/namespace')
owl_graph.bind('catalog', "http://www.semanticweb.org/hrishi/ontologies/2023/4/untitled-ontology-10#")
owl_graph.bind('person', "http://www.semanticweb.org/hrishi/ontologies/2023/4/untitled-ontology-10#")

# iterate movies
for movie in root.findall('movies/movie'):
    movie_id = movie.attrib['id']
    movie_title = movie.find('title').text
    movie_year = movie.find('year').text

    # add movie triples to the graph
    owl_graph.add((
        (ns.catalog[movie_id], RDF.type, ns.catalog['Movie']),
        (ns.catalog[movie_id], ns.predicates['title'], Literal(movie_title)),
        (ns.catalog[movie_id], ns.predicates['year'], Literal(movie_year))
    ))

    # add genre to the graph
    for genre in movie.findall('genre'):
        owl_graph.add((
            (ns.catalog[movie_id], ns.predicates['genre'], Literal(genre.text))
        ))

    # add plot to the graph
    plot = movie.find('plot').text
    owl_graph.add((
        (ns.catalog[movie_id], ns.predicates['plot'], Literal(plot))
    ))

    # add country to the graph
    country = movie.find('country').text
    owl_graph.add((
        (ns.catalog[movie_id], ns.predicates['country'], Literal(country))
    ))

    # add language to the graph
    language = movie.find('language').text
    owl_graph.add((
        (ns.catalog[movie_id], ns.predicates['language'], Literal(language))
    ))

    # add runtime to the graph
    runtime = movie.find('runtime').text
    owl_graph.add((
        (ns.catalog[movie_id], ns.predicates['runtime'], Literal(runtime))
    ))

    # add rating to the graph
    rating = movie.find('rating').text
    owl_graph.add((
        (ns.catalog[movie_id], ns.predicates['rating'], Literal(rating))
    ))

    # add actors to the graph
    for actor in movie.findall('actor'):
        actor_id = actor.attrib['id']
        actor_name = actor.text
        owl_graph.add((
            (ns.catalog[movie_id], ns.predicates['hasActor'], ns.person[actor_id]),
            (ns.person[actor_id], RDF.type, ns.person['Actor']),
            (ns.person[actor_id], ns.predicates['name'], Literal(actor_name))
        ))

    # add director to the graph
    director = movie.find('director')
    director_id = director.attrib['id']
    director_name = director.text
    owl_graph.add((
        (ns.catalog[movie_id], ns.predicates['hasDirector'], ns.person[director_id]),
        (ns.person[director_id],RDF.type,ns.person['Director']),
        (ns.person[director_id], ns.predicates['name'], Literal(director_name))
    ))

    # add writers to the graph
    for writer in movie.findall('writers/writer'):
        writer_id = writer.attrib['id']
        writer_name = writer.text
        owl_graph.add((
            (ns.catalog[movie_id], ns.predicates['hasWriter'], ns.person[writer_id]),
            (ns.person[writer_id], RDF.type, ns.person['Writer']),
            (ns.person[writer_id], ns.predicates['name'], Literal(writer_name))
        ))

    # add awards to the graph
    for award in movie.findall('awards/award'):
        owl_graph.add((
            (ns.catalog[movie_id], ns.predicates['hasAward'], Literal(award.text))
        ))

# iterate each person and add triples to the graph

for person in root.findall('persons/person'):
    person_id = person.attrib['id']
    person_name = person.find('name').text
    person_birth_date = person.find('birth_date').text
    owl_graph.add((
        (ns.person[person_id], RDF.type, ns.person['Person']),
        (ns.person[person_id], ns.predicates['name'], Literal(person_name)),
        (ns.person[person_id], ns.predicates['birth_date'], Literal(person_birth_date))
    ))

# write data to the owl file
owl_graph.serialize(destination='moviesOntology.owl', format='xml')

textfile = open("CS22M047_infered.txt", "w")

for s, p, o in owl_graph:
    print('Subject - '+str(s)+'\n','predicate - '+str(p)+'\n','object - '+str(o))
    print("------------------------------------------------------------------------------------")
    textfile.write('Subject - '+str(s)+'\n')
    textfile.write('predicate - '+str(p)+'\n')
    textfile.write('object - '+str(o)+'\n')
    textfile.write("------------------------------------------------------------------------------------\n")
textfile.close()
