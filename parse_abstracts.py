__author__ = 'petr'


from lxml import etree
from time import time
import networkx as nx
import matplotlib.pyplot as plt


class cArticle(object):
    def __init__(self):
        self.title = ''
        self.abstract = ''
        self.authors = []
        self.PMID = 0
        self.dictionary = {}


def parse_articles(path):
    tree = etree.parse(path)
    root = tree.getroot()

    articles_list = []

    for element in root.iter(tag=etree.Element):
        # print("%s - %s" % (element.tag, element.text))
        if element.tag == 'MedlineCitation':
            article = cArticle()
            for child in element:
                if child.tag == 'PMID':
                    article.PMID = child.text
                if child.tag == 'Article':
                    for sub_article in child:
                        if sub_article.tag == 'ArticleTitle':
                            article.title = sub_article.text
                        if sub_article.tag == 'Abstract':
                            for sub_element in sub_article:
                                if sub_element.tag == 'AbstractText':
                                    article.abstract += sub_element.text
                        if sub_article.tag == 'AuthorList':
                            for sub_author in sub_article:
                                last_name = ''
                                for author in sub_author:
                                    if author.tag == 'LastName':
                                        last_name = author.text
                                    elif author.tag == 'Initials':
                                        name = ' '.join((last_name, author.text))
                                        article.authors.append(name)
                    articles_list.append(article)
    return articles_list


start = time()

path = './human_gut_microbiota.xml'

articles_list = parse_articles(path)

authors_graph = nx.Graph()
articles_graph = nx.Graph()

for article in articles_list[:]:
    authors_graph.add_nodes_from(article.authors)
    for author_1 in article.authors:
        for author_2 in article.authors:
            if author_1 != author_2:
                authors_graph.add_edge(author_1, author_2, {'weight': 1})

                # print '_' * 80
                # print article.title
                # print 'PMID=', article.PMID
                # for author in article.authors:
                #     print author
                # print article.abstract
                #

for i in range(len(articles_list[:])):
    for j in range(i+1, len(articles_list[:])):
        if articles_list[i] != articles_list[j]:
            articles_graph.add_node(articles_list[i].PMID)
            articles_graph.add_node(articles_list[j].PMID)
        articles_graph.add_edge(articles_list[i].PMID, articles_list[j].PMID, {'weight': 1})
        for author in articles_list[j].authors:
            if author in articles_list[i].authors:
                articles_graph[articles_list[i].PMID][articles_list[j].PMID]['weight'] += 1


for edge in articles_graph.edges():
    if articles_graph[edge[0]][edge[1]]['weight'] <= 5:
        articles_graph.remove_edge(*edge)
for node in articles_graph.nodes():
    if len(articles_graph.neighbors(node)) == 0:
        articles_graph.remove_node(node)

nx.draw(articles_graph)
plt.show()

end = time()

print end - start
