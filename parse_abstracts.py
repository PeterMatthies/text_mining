__author__ = 'petr'

from lxml import etree
from bacteria.find_bacteria import find_bacteria
from diseases.find_diseases import find_diseases
from nltk.stem import SnowballStemmer as Ss
import nltk


with open('./exclusions/200_most_common_words.txt') as f:
    exclude = f.readlines()
with open('./exclusions/list_of_prepositions.txt') as f:
    exclude += f.readlines()
with open('./exclusions/other.txt') as f:
    exclude += f.readlines()
exclude = map(lambda x: (x.strip().lower(), 0), exclude)
exclude = dict(exclude)


class ArticleClass(object):
    def __init__(self):
        self.title = ''
        self.abstract = ''
        self.authors = []
        self.year = 0
        self.disease_ids = []
        self.disease_names = []
        self.bacteria = []
        self.PMID = 0
        self.dictionary = {}

    def get_bacteria(self):
        bacteria_list = find_bacteria(self.abstract)
        if len(bacteria_list) != 0:
            for item in bacteria_list:
                self.bacteria.append(item)

    def get_diseases(self):
        self.disease_ids, self.disease_names = find_diseases(' '.join((self.title, self.abstract)))

    def get_dictionary(self):
        stemmer = Ss('english')
        words = nltk.word_tokenize(self.abstract)
        words = filter(lambda x: x.isalpha(), words)
        words = filter(lambda x: len(x) > 1, words)
        words = map(lambda x: x.lower(), words)
        for word in words:
            stemmed_word = stemmer.stem(word)
            if word not in exclude:
                if stemmed_word not in self.dictionary:
                    self.dictionary[word] = 0
                else:
                    self.dictionary[stemmed_word] += 1

        self.dictionary = self.dictionary.items()
        self.dictionary = sorted(self.dictionary, key=lambda x: x[1], reverse=True)
        # print self.dictionary[:100]
        self.dictionary = dict(self.dictionary[:10])


def parse_articles(path):
    tree = etree.parse(path)
    root = tree.getroot()

    articles_list = []
    a_count = 0
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
                        # date.clear()
                if citation_child is not None and citation_child.tag == 'Article':
                    for sub_article in citation_child:
                        if sub_article is not None and sub_article.tag == 'ArticleTitle':
                            article.title = sub_article.text
                        if sub_article is not None and sub_article.tag == 'Abstract':
                            for sub_abstract in sub_article:
                                if sub_abstract is not None and sub_abstract.tag == 'AbstractText':
                                    article.abstract += ''.join((' ', sub_abstract.text))
                                # sub_abstract.clear()
                        if sub_article is not None and sub_article.tag == 'AuthorList':
                            for sub_author in sub_article:
                                last_name = ''
                                for author in sub_author:
                                    if author is not None and author.tag == 'LastName':
                                        last_name = author.text
                                    elif author is not None and author.tag == 'Initials':
                                        name = ' '.join((last_name, author.text))
                                        article.authors.append(name)
                                    # author.clear()
                                # sub_author.clear()
                        # sub_article.clear()
                # citation_child.clear()
            if len(articles_list) < 3000:
                articles_list.append(article)
        # element.clear()
    return articles_list
