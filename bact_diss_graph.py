__author__ = 'petr'

from time import time
import igraph as ig
from parse_abstracts import parse_articles

start = time()

path = './human_gut_microbiota.xml'

art_list = parse_articles(path)

bact_diseases_graph = ig.Graph()

for art in art_list[:]:
    art.get_bacteria()
    art.get_diseases()
    # tokens = nltk.word_tokenize(art.abstract)
    # tagged = nltk.pos_tag(tokens)
    # entities = nltk.chunk.ne_chunk(tagged)
    # print entities


vertex_weights = {}
edges_weights = {}
vertex_types = []

for article in art_list:
    if len(article.bacteria) > 0:
        for bacteria in article.bacteria:
            for b in bacteria[1]:
                if 'name' not in bact_diseases_graph.vs.attributes():
                    bact_diseases_graph.add_vertex(b[0])
                    vertex_weights[b[0]] = b[1]
                    vertex_types.append('bacteria')
                else:
                    if b[0] not in bact_diseases_graph.vs['name']:
                        bact_diseases_graph.add_vertex(b[0])
                        vertex_weights[b[0]] = b[1]
                        vertex_types.append('bacteria')
                    else:
                        vertex_weights[b[0]] += b[1]
    if len(article.disease_names) > 0:
        for disease_id, disease in zip(article.disease_ids, article.disease_names):
            if disease != 'disease' and 'syndrome':
                if 'name' not in bact_diseases_graph.vs.attributes():
                    bact_diseases_graph.add_vertex(disease)
                    vertex_weights[disease] = article.disease_ids[disease_id]
                    vertex_types.append('disease')
                else:
                    if disease not in bact_diseases_graph.vs['name']:
                        bact_diseases_graph.add_vertex(disease)
                        vertex_weights[disease] = article.disease_ids[disease_id]
                        vertex_types.append('disease')
                    else:
                        vertex_weights[disease] += article.disease_ids[disease_id]
    if len(article.bacteria) and len(article.disease_names) > 0:
        for bacteria in article.bacteria:
            for b in bacteria[1]:
                for disease in article.disease_names:
                    if disease != 'disease' and 'syndrome':
                        if not bact_diseases_graph.are_connected(b[0], disease):
                            bact_diseases_graph.add_edge(b[0], disease)
                            edges_weights[' '.join((b[0], disease))] = 1
                        else:
                            edges_weights[' '.join((b[0], disease))] += 1


print bact_diseases_graph.vs['name']

print vertex_types
print vertex_weights
print edges_weights
bact_diseases_graph.vs['type'] = vertex_types
color_dict = {'bacteria': 'red', 'disease': 'blue'}
bact_diseases_graph.vs['color'] = [color_dict[type_] for type_ in bact_diseases_graph.vs['type']]
bact_diseases_graph.vs['label'] = bact_diseases_graph.vs['name']

l1 = bact_diseases_graph.layout('circular')
ig.plot(bact_diseases_graph, layout=l1, bbox=(4000, 4000), margin=20)

end = time()
print end - start
