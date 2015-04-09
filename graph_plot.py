__author__ = 'petr'


from time import time
import networkx as nx
import matplotlib.pyplot as plt
from parse_abstracts import parse_articles

start = time()

path = './human_gut_microbiota.xml'

art_list = parse_articles(path)

authors_graph = nx.Graph()
articles_graph = nx.Graph()

for art in art_list[:]:
    # authors_graph.add_nodes_from(art.authors)
    #     for author_1 in art.authors:
    #         for author_2 in art.authors:
    #             if author_1 != author_2:
    #                 authors_graph.add_edge(author_1, author_2, {'weight': 1})

    art.get_bacteria()
    art.get_diseases()
    # print '_' * 80
    # print art.title
    # print art.year
    # print 'PMID=', art.PMID
    # for auth in art.authors:
    #     print auth
    # print art.abstract
    # print art.bacteria
    # print art.disease_ids
    # print art.disease_names


for i in range(len(art_list[:])):
    for j in range(i + 1, len(art_list[:])):
        if art_list[j].bacteria is not None and art_list[i].bacteria is not None:
            if art_list[i] != art_list[j]:
                articles_graph.add_node(art_list[i].year + '-' + art_list[i].PMID)
                articles_graph.add_node(art_list[j].year + '-' + art_list[j].PMID)
            articles_graph.add_edge(art_list[i].year + '-' + art_list[i].PMID, art_list[j].year + '-' + art_list[j].PMID,
                                    {'weight': 1})
            for author in art_list[j].authors:
                if author in art_list[i].authors:
                    articles_graph[art_list[i].year + '-' + art_list[i].PMID][art_list[j].year + '-' +
                                                                              art_list[j].PMID]['weight'] += 1
            matching_bacteria = []
            for item in art_list[j].bacteria:
                for bacteria in item[1]:
                    matching_bacteria.append([bact[0] for it in art_list[i].bacteria for bact in it[1]
                                              if bact[0] == bacteria[0]])
            len_bact = len(matching_bacteria)
            articles_graph[art_list[i].year + '-' + art_list[i].PMID][art_list[j].year + '-' +
                                                                      art_list[j].PMID]['weight'] += len_bact

for edge in articles_graph.edges():
    if articles_graph[edge[0]][edge[1]]['weight'] <= 10:
        articles_graph.remove_edge(*edge)
for node in articles_graph.nodes():
    if len(articles_graph.neighbors(node)) == 0:
        articles_graph.remove_node(node)
max_, max_node = 0, 0
for node in articles_graph.nodes():
    neighbors_len = len(articles_graph.neighbors(node))
    if max_ < neighbors_len:
        max_ = neighbors_len
        max_node = node
print max_, max_node
# nx.draw(articles_graph)
# plt.show()

end = time()

print end - start
