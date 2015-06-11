__author__ = 'petr'

from time import time
import igraph as ig
from parse_abstracts import parse_articles
import matplotlib.pyplot as plt

start = time()

path = './human_gut_microbiota.xml'

art_list = parse_articles(path)

bact_diseases_graph = ig.Graph()
authors_bd = ig.Graph()
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
    for author in article.authors:                      # adding authors from current article to the graph
            author = author.encode('utf8')
            if 'name' not in bact_diseases_graph.vs.attributes():
                bact_diseases_graph.add_vertex(author)
                vertex_weights[author] = 1
                vertex_types.append('author')
            else:
                if author not in bact_diseases_graph.vs['name']:
                    bact_diseases_graph.add_vertex(author)
                    vertex_weights[author] = 1
                    vertex_types.append('author')
                else:
                    vertex_weights[author] += 1
    if len(article.bacteria) > 0:                       # adding bacteria from current article to the graph
        for bacteria in article.bacteria:
            for b in bacteria[1]:
                if 'name' not in bact_diseases_graph.vs.attributes():
                    bact_diseases_graph.add_vertex(b[0].encode('utf8'))
                    vertex_weights[b[0].encode('utf8')] = b[1]
                    vertex_types.append('bacteria')
                else:
                    if b[0].encode('utf8') not in bact_diseases_graph.vs['name']:
                        bact_diseases_graph.add_vertex(b[0].encode('utf8'))
                        vertex_weights[b[0].encode('utf8')] = b[1]
                        vertex_types.append('bacteria')
                    else:
                        vertex_weights[b[0].encode('utf8')] += b[1]
                for author in article.authors:          # adding edges between authors and bacteria
                    author = author.encode('utf8')
                    if not bact_diseases_graph.are_connected(author, b[0].encode('utf8')):
                        bact_diseases_graph.add_edge(author, b[0].encode('utf8'))
                        edges_weights['_'.join((author, b[0].encode('utf8')))] = 1
                    else:
                        edges_weights['_'.join((author, b[0].encode('utf8')))] += 1

    if len(article.disease_names) > 0:                  # adding diseases from current article to the graph
        for disease_id, disease in zip(article.disease_ids, article.disease_names):
            disease = disease.encode('utf8')
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
                for author in article.authors:           # adding edges between authors and diseases
                    author = author.encode('utf8')
                    if not bact_diseases_graph.are_connected(author, disease):
                        bact_diseases_graph.add_edge(author, disease)
                        edges_weights['_'.join((author, disease))] = 1
                    else:
                        edges_weights['_'.join((author, disease))] += 1
    if len(article.bacteria) and len(article.disease_names) > 0:   # adding edges between bacteria and diseases
        for bacteria in article.bacteria:
            for b in bacteria[1]:
                for disease in article.disease_names:
                    if disease != 'disease' and 'syndrome':
                        if not bact_diseases_graph.are_connected(disease, b[0].encode('utf8')):
                            bact_diseases_graph.add_edge(disease, b[0].encode('utf8'))
                            edges_weights['_'.join((disease, b[0].encode('utf8')))] = 1
                        else:
                            edges_weights['_'.join((disease, b[0].encode('utf8')))] += 1


#
# print bact_diseases_graph.vs['name']
#
# print vertex_types
# print vertex_weights
# print edges_weights

bact_diseases_graph.vs['type'] = vertex_types
color_dict = {'bacteria': 'red', 'disease': 'blue', 'author': 'green'}
bact_diseases_graph.vs['color'] = [color_dict[type_] for type_ in bact_diseases_graph.vs['type']]
bact_diseases_graph.vs['label'] = bact_diseases_graph.vs['name']


print len(vertex_weights), len(edges_weights)

# getting lists of all authors, bacteria and diseases from all articles
all_bacteria = list(set([b[0].encode('utf8') for article in art_list
                         for bacteria in article.bacteria for b in bacteria[1]
                         if len(article.disease_names) > 0 and len(article.bacteria) > 0]))
all_authors = list(set([author.encode('utf8') for article in art_list for author in article.authors
                        if len(article.disease_names) > 0 and len(article.bacteria) > 0]))
all_diseases = list(set([disease.encode('utf8') for article in art_list for disease in article.disease_names
                         if len(article.disease_names) > 0 and len(article.bacteria) > 0]))


print all_authors
print all_bacteria
print all_diseases


for a in all_authors:                        # setting weights to zero
    for bacteria in all_bacteria:
        if '_'.join((a, bacteria)) not in edges_weights.keys():
            edges_weights['_'.join((a, bacteria))] = 0

    for d in all_diseases:
        if '_'.join((a, d)) not in edges_weights.keys():
            edges_weights['_'.join((a, d))] = 0

for d in all_diseases:
    for bacteria in all_bacteria:
        if '_'.join((d, bacteria)) not in edges_weights.keys():
            edges_weights['_'.join((d, bacteria))] = 0


bact_auth = []
bact_dis = []
auth_dis = []

for bacteria in all_bacteria:                 # bacteria from diseases, authors
    bact_auth.append(sum([edges_weights['_'.join((a, bacteria))] for a in all_authors]))
    bact_dis.append(sum([edges_weights['_'.join((d, bacteria))] for d in all_diseases]))

with open('bacteria_ad_1.txt', 'w') as f:
    for b, x, y in zip(all_bacteria, bact_auth, bact_dis):
        f.write(b + '\t' + '\t'.join((str(x), str(y))) + '\n')

bact_auth = []
bact_dis = []
auth_dis = []


for a in all_authors:                         # authors from bacteria, diseases
    bact_auth.append(sum([edges_weights['_'.join((a, b))] for b in all_bacteria]))
    auth_dis.append(sum([edges_weights['_'.join((a, d))] for d in all_diseases]))

with open('authors_bd_1.txt', 'w') as f:
    for a, x, y in zip(all_authors, bact_auth, auth_dis):
        f.write(a + '\t' + '\t'.join((str(x), str(y))) + '\n')

bact_auth = []
bact_dis = []
auth_dis = []

for disease in all_diseases:                  # diseases from authors, bacteria
    auth_dis.append(sum([edges_weights['_'.join((a, d))] for a in all_authors]))
    bact_dis.append(sum([edges_weights['_'.join((d, b))] for b in all_bacteria]))


with open('diseases_ab_1.txt', 'w') as f:
    for d, x, y in zip(all_diseases, auth_dis, bact_dis):
        f.write(d + '\t' + '\t'.join((str(x), str(y))) + '\n')


# plt.scatter(b_a, a_d)
# plt.show()
#
# plt.scatter(a_d, d_b)
# plt.show()
#

#
# l1 = bact_diseases_graph.layout('circular')
# l2 = bact_diseases_graph.layout('kk')
# plot = ig.plot(bact_diseases_graph, layout=l1, bbox=(6000, 6000), margin=20)
#
# plot.save('auth_bact_dis_graph4.png')
end = time()
print end - start
