__author__ = 'petr'


from time import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from parse_abstracts import parse_articles
import nltk


start = time()

path = './human_gut_microbiota.xml'

art_list = parse_articles(path)

bact_diseases_graph = nx.Graph()

for art in art_list[:]:
    art.get_bacteria()
    art.get_diseases()
    # tokens = nltk.word_tokenize(art.abstract)
    # tagged = nltk.pos_tag(tokens)
    # entities = nltk.chunk.ne_chunk(tagged)
    # print entities
bact = []
diss = []

for article in art_list:
    if len(article.bacteria) > 0:
        for bacteria in article.bacteria:
            for b in bacteria[1]:
                if b[0] not in bact:
                    bact.append(b[0])
                bact_diseases_graph.add_node(b[0])
                bact_diseases_graph.node[b[0]]['weight'] = 0
    if len(article.disease_names) > 0:
        for disease in article.disease_names:
            if disease != 'disease' and 'syndrome':
                if disease not in diss:
                    diss.append(disease)
                bact_diseases_graph.add_node(disease)
                bact_diseases_graph.node[disease]['weight'] = 1
for article in art_list:
    if len(article.bacteria) > 0:
        for bacteria in article.bacteria:
            for b in bacteria[1]:
                bact_diseases_graph.node[b[0]]['weight'] += b[1]
                bact_diseases_graph.node[b[0]]['color'] = 'r'
    if len(article.disease_names) > 0:
        for disease_id, disease in zip(article.disease_ids, article.disease_names):
            if disease != 'disease' and 'syndrome':
                bact_diseases_graph.node[disease]['weight'] += article.disease_ids[disease_id]
                bact_diseases_graph.node[disease]['color'] = 'b'

    if len(article.bacteria) and len(article.disease_names) > 0:
        for bacteria in article.bacteria:
            for b in bacteria[1]:
                for disease in article.disease_names:
                    if disease != 'disease' and 'syndrome':
                        bact_diseases_graph.add_edge(b[0], disease)
                        if 'weight' in bact_diseases_graph[b[0]][disease]:
                            bact_diseases_graph[b[0]][disease]['weight'] += 1
                        else:
                            bact_diseases_graph[b[0]][disease]['weight'] = 1

bact_diseases_graph_filtered = nx.Graph()

for edge in bact_diseases_graph.edges():
    if bact_diseases_graph[edge[0]][edge[1]]['weight'] >= 11:
        bact_diseases_graph_filtered.add_node(edge[0])
        bact_diseases_graph_filtered.node[edge[0]]['weight'] = bact_diseases_graph.node[edge[0]]['weight']
        bact_diseases_graph_filtered.node[edge[0]]['color'] = bact_diseases_graph.node[edge[0]]['color']
        bact_diseases_graph_filtered.add_node(edge[1])
        bact_diseases_graph_filtered.node[edge[1]]['weight'] = bact_diseases_graph.node[edge[1]]['weight']
        bact_diseases_graph_filtered.node[edge[1]]['color'] = bact_diseases_graph.node[edge[1]]['color']
        bact_diseases_graph_filtered.add_edge(edge[0], edge[1])
        bact_diseases_graph_filtered[edge[0]][edge[1]]['weight'] = bact_diseases_graph[edge[0]][edge[1]]['weight']
        bact_diseases_graph.remove_edge(*edge)

pos = nx.pygraphviz_layout(bact_diseases_graph, prog='neato')
# pos = nx.circular_layout(bact_diseases_graph, scale=100)

sizes_filtered = [bact_diseases_graph_filtered.node[node]['weight']*10 for node in bact_diseases_graph_filtered.nodes()]
labels_filtered = {edge: bact_diseases_graph_filtered[edge[0]][edge[1]]['weight'] for edge in bact_diseases_graph_filtered.edges()}
colors_filtered = [bact_diseases_graph_filtered.node[node]['color'] for node in bact_diseases_graph_filtered.nodes()]
# nx.draw(bact_diseases_graph_filtered, pos, node_size=sizes_filtered, node_color=colors_filtered)
# nx.draw_networkx_edge_labels(bact_diseases_graph, pos, edge_labels=labels_filtered)
# plt.show()
#

#
# for node in bact_diseases_graph.nodes():
#     if len(bact_diseases_graph.neighbors(node)) == 0:
#         bact_diseases_graph.remove_node(node)
#
#
#
#
# bact_diseases_graph.remove_node('disease')
# bact_diseases_graph.remove_node('syndrome')
sizes = [bact_diseases_graph.node[node]['weight']*10 for node in bact_diseases_graph.nodes()]
colors = [bact_diseases_graph.node[node]['color'] for node in bact_diseases_graph.nodes()]
labels = {edge: bact_diseases_graph[edge[0]][edge[1]]['weight'] for edge in bact_diseases_graph.edges()}
#
# max_, max_node = 0, 0
# for node in bact_diseases_graph.nodes():
#     neighbors_len = len(bact_diseases_graph.neighbors(node))
#     if max_ < neighbors_len:
#         max_ = neighbors_len
#         max_node = node
# print max_, max_node
#
# nx.draw(bact_diseases_graph, pos, node_size=sizes, node_color=colors)
# nx.draw_networkx_edge_labels(bact_diseases_graph, pos, edge_labels=labels)
# plt.show()


# bact_diseases_matrix = np.zeros((len(bact), len(diss)))
# print bact
# print diss
# for i, bac in enumerate(bact):
#     for j, dis in enumerate(diss):
#         if (bac, dis) in bact_diseases_graph.edges():
#             bact_diseases_matrix[i][j] = labels[(bac, dis)]
# print bact_diseases_matrix.shape

with open('bact_diseases.txt', 'w') as f:
    for edge in bact_diseases_graph.edges():
        f.write('\t'.join((edge[0], 'bact_disease', edge[1], bact_diseases_graph.node[edge[0]]['color'],
                          bact_diseases_graph.node[edge[1]]['color'])) + '\n')


# with open('bact_diseases_matrix.txt', 'w') as f:
#     f.write('' + '\t' + '\t'.join(diss) + '\n')
#     for bact, row in zip(bact, bact_diseases_matrix):
#             row = [str(elem) for elem in row]
#             f.write(bact+ '\t' + '\t'.join(row) + '\n')


end = time()
print end - start




