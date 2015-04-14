__author__ = 'petr'


from time import time
import networkx as nx
import matplotlib.pyplot as plt
from parse_abstracts import parse_articles


start = time()

path = './human_gut_microbiota.xml'

art_list = parse_articles(path)

bact_diseases_graph = nx.Graph()

for art in art_list[:]:
    art.get_bacteria()
    art.get_diseases()

for article in art_list:
    if article.bacteria is not None:
        for bacteria in article.bacteria:
            bact_diseases_graph.add_node(bacteria[1][0][0])
            bact_diseases_graph.node[bacteria[1][0][0]]['weight'] = 0
    if article.disease_names is not None:
        for disease in article.disease_names:
            bact_diseases_graph.add_node(disease)
            bact_diseases_graph.node[disease]['weight'] = 1


for article in art_list:
    if article.bacteria is not None:
        for bacteria in article.bacteria:
            bact_diseases_graph.node[bacteria[1][0][0]]['weight'] += bacteria[1][0][1]
            bact_diseases_graph.node[bacteria[1][0][0]]['color'] = 'r'
    if article.disease_names is not None:
        for disease_id, disease in zip(article.disease_ids, article.disease_names):
            bact_diseases_graph.node[disease]['weight'] += article.disease_ids[disease_id]
            bact_diseases_graph.node[disease]['color'] = 'b'

    if article.bacteria and article.disease_names is not None:
        for bacteria in article.bacteria:
            for disease in article.disease_names:
                bact_diseases_graph.add_edge(bacteria[1][0][0], disease)

for node in bact_diseases_graph.nodes():
    if len(bact_diseases_graph.neighbors(node)) == 0:
        bact_diseases_graph.remove_node(node)

bact_diseases_graph.remove_node('disease')
bact_diseases_graph.remove_node('syndrome')
sizes = [bact_diseases_graph.node[node]['weight']*10 for node in bact_diseases_graph.nodes()]
colors = [bact_diseases_graph.node[node]['color'] for node in bact_diseases_graph.nodes()]
print sizes
nx.draw(bact_diseases_graph, node_size=sizes, node_color=colors)
plt.show()

end = time()

print end - start