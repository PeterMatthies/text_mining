__author__ = 'petr'


from parse_abstracts import parse_articles
from time import time
import numpy as np


def get_articles_info(articles_list):
    for art in articles_list[:]:
        art.get_bacteria()
        art.get_diseases()
        art.get_dictionary()
    return articles_list

start = time()

path_microbiota = './human_gut_microbiota.xml'
path_other = './mass_spectrometry_1.xml'

art_list_microbiota = parse_articles(path_microbiota)
art_list_other = parse_articles(path_other)

art_list_mbt = get_articles_info(art_list_microbiota)
art_list_otr = get_articles_info(art_list_other)

art_list_full = art_list_mbt + art_list_otr

terms_docs_dict = {}

terms_list = [article.dictionary.keys() for article in art_list_full]
terms_list = reduce(lambda x, y: x + y, terms_list)
terms_list = list(set(terms_list))

most_used_terms = terms_list[:]

print most_used_terms

for i, a in enumerate(art_list_full):
    used_terms_dict = {term: a.dictionary[term] for term in most_used_terms if term in a.dictionary.keys()}
    unused_terms_dict = {term: 0 for term in most_used_terms if term not in a.dictionary.keys()}
    used_terms_dict.update(unused_terms_dict)
    terms_docs_dict['doc'+str(i+1)] = used_terms_dict

terms_docs_matrix = np.array([terms_docs_dict[d][term] for d in terms_docs_dict
                              for term in terms_docs_dict[d]]).reshape(len(most_used_terms), len(terms_docs_dict))

print terms_docs_matrix.shape

u, s, v = np.linalg.svd(terms_docs_matrix)

S = np.diag(s[:2])
print S

print s

X = u[:, :2].dot(S).dot(v[:2])
print '_' * 80
print terms_docs_matrix

print
print '_' * 80
np.set_printoptions(precision=3, suppress=True)
print X

with open('term_docs_matrix_full.txt', 'w') as f:
    for i, row in enumerate(terms_docs_matrix):
        row = [str(r) for r in row]
        f.write('\t' + '\t'.join(row) + '\n')
# m = terms_docs_matrix.shape[1]
# similarity_matrix = np.zeros((m, m))
# for i, term_vector in enumerate(X.T):
#     for j, doc_vector in enumerate(X.T):
#         if np.linalg.norm(X.T[i]) == 0 or np.linalg.norm(X.T[j]) == 0:
#             similarity = X.T[i].dot(X.T[j])
#         else:
#             similarity = X.T[i].dot(X.T[j]) /\
#                 (np.linalg.norm(X.T[i]) * np.linalg.norm(X.T[j]))
#         similarity_matrix[i][j] = similarity
#
# distance_matrix = np.zeros((m, m))
#
# for i, similarity_row in enumerate(similarity_matrix):
#     for j, similarity_column in enumerate(similarity_matrix.T):
#         distance_matrix[i][j] = np.nan_to_num(np.sqrt(similarity_matrix[i][i] -
#                                               2*similarity_matrix[i][j] +
#                                               similarity_matrix[j][j]))
# print '-'*100
# print distance_matrix
# column_names = terms_docs_dict.keys()
# # document_numbers = [name.split(':')[0] for name in column_names]
# # row_names = terms_list
# with open('distance_matrix_full.txt', 'w') as f:
#     f.write('distance_matrix \t' + '\t'.join(column_names) + '\n')
#     for i, row in enumerate(distance_matrix):
#         row = [str(r) for r in row]
#         f.write(column_names[i] + '\t' + '\t'.join(row) + '\n')

end = time()
print end - start
