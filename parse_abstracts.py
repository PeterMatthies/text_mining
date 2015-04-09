__author__ = 'petr'

from lxml import etree
from bacteria.find_bacteria import find_bacteria
from diseases.find_diseases import find_diseases


class ArticleClass(object):
    def __init__(self):
        self.title = ''
        self.abstract = ''
        self.authors = []
        self.year = 0
        self.disease_ids = []
        self.disease_names  =[]
        self.bacteria = []
        self.PMID = 0
        self.dictionary = {}

    def get_bacteria(self):
        bacteria_list = find_bacteria(self.abstract)
        if len(bacteria_list) != 0:
            for item in bacteria_list:
                self.bacteria.append(item)

    def get_diseases(self):
        self.disease_ids, self.disease_names = find_diseases(self.abstract)


def parse_articles(path):
    tree = etree.parse(path)
    root = tree.getroot()

    articles_list = []

    for element in root.iter(tag=etree.Element):
        if element is not None and element.tag == 'MedlineCitation':
            article = ArticleClass()
            for citation_child in element:
                if citation_child is not None and citation_child.tag == 'PMID':
                    article.PMID = citation_child.text
                if citation_child is not None and citation_child.tag == 'DateCreated':
                    for date in citation_child:
                        if date is not None and date.tag == 'Year':
                            article.year = date.text
                if citation_child is not None and citation_child.tag == 'Article':
                    for sub_article in citation_child:
                        if sub_article is not None and sub_article.tag == 'ArticleTitle':
                            article.title = sub_article.text
                        if sub_article is not None and sub_article.tag == 'Abstract':
                            for sub_abstract in sub_article:
                                if sub_abstract is not None and sub_abstract.tag == 'AbstractText':
                                    article.abstract += sub_abstract.text
                        if sub_article is not None and sub_article.tag == 'AuthorList':
                            for sub_author in sub_article:
                                last_name = ''
                                for author in sub_author:
                                    if author is not None and author.tag == 'LastName':
                                        last_name = author.text
                                    elif author is not None and author.tag == 'Initials':
                                        name = ' '.join((last_name, author.text))
                                        article.authors.append(name)
                    articles_list.append(article)
    return articles_list