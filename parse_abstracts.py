__author__ = 'petr'


from lxml import etree
from time import time
import networkx as nx
import matplotlib.pyplot as plt


class ArticleClass(object):
    def __init__(self):
        self.title = ''
        self.abstract = ''
        self.authors = []
        self.year = 0
        self.deseases = []
        self.PMID = 0
        self.dictionary = {}


def parse_articles(path):
    tree = etree.parse(path)
    root = tree.getroot()

    articles_list = []

    for element in root.iter(tag=etree.Element):
        # print("%s - %s" % (element.tag, element.text))
        if element.tag == 'MedlineCitation':
            article = ArticleClass()
            for medline_citation in element:
                if medline_citation.tag == 'PMID':
                    article.PMID = medline_citation.text
                if medline_citation.tag == 'DateCreated':
                    for date in medline_citation:
                        if date.tag == 'Year':
                            article.year = date.text
                if medline_citation.tag == 'Article':
                    for sub_article in medline_citation:
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

art_list = parse_articles(path)

authors_graph = nx.Graph()
articles_graph = nx.Graph()

for art in art_list[:]:
    authors_graph.add_nodes_from(art.authors)
    for author_1 in art.authors:
        for author_2 in art.authors:
            if author_1 != author_2:
                authors_graph.add_edge(author_1, author_2, {'weight': 1})

    print '_' * 80
    print art.title
    print art.year
    print 'PMID=', art.PMID
    for author in art.authors:
        print author
    print art.abstract


# for i in range(len(art_list[:])):
#     for j in range(i+1, len(art_list[:])):
#         if art_list[i] != art_list[j]:
#             articles_graph.add_node(art_list[i].PMID)
#             articles_graph.add_node(art_list[j].PMID)
#         articles_graph.add_edge(art_list[i].PMID, art_list[j].PMID, {'weight': 1})
#         for author in art_list[j].authors:
#             if author in art_list[i].authors:
#                 articles_graph[art_list[i].PMID][art_list[j].PMID]['weight'] += 1
#
#
# for edge in articles_graph.edges():
#     if articles_graph[edge[0]][edge[1]]['weight'] <= 5:
#         articles_graph.remove_edge(*edge)
# for node in articles_graph.nodes():
#     if len(articles_graph.neighbors(node)) == 0:
#         articles_graph.remove_node(node)

# nx.draw(articles_graph)
# plt.show()

end = time()

print end - start
