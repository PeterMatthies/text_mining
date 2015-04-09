__author__ = 'yarygin_konstantin'
# -*- coding: UTF-8 -*-

import re


class WTreeNode(object):
    def __init__(self):
        self.is_end = False
        self.children = {}
# Например:

# Имена болезней:
#
#   squamous cell carcinoma
#   squamous carcinoma
#   squamous cell cancer
#   squamous cell carcinoma (disorder)
#   squamous cell carcinoma (morphologic abnormality)
#   squamous cell carcinoma NOS (morphologic abnormality)
#
#
# Структура дерева:
#
#            |-- carcinoma*              |-- (disorder)*
# squamous --|                           |
#            |-- cell --|-- carcinoma* --|-- (morphologic -- abnormality)*
#                       |                |
#                       |-- cancer*      |-- NOS -- (morphologic -- abnormality)*
#
# символ * означает конец какого-либо названия болезни


# из онтологии берем id и названия болезней с синонимами
with open('diseases/HumanDO.obo') as f:
    data = [[]]
    for line in f.readlines():
        if line == '\n':
            data.append([])
        else:
            data[-1].append(line.strip())

data = [item for item in data if (item != [] and item[0] == '[Term]')]

disease_by_DOID = {} # key - DOID; value - disease names
for item in data:
    item_DOID = ''
    for line in item:
        if line.startswith('id:'):
            match = re.match('^id: DOID:(\d+)', line)
            item_DOID = match.group(1).strip()
            disease_by_DOID[item_DOID] = []
            continue
        if line.startswith('name:'):
            match = re.match('^name: (.*)', line)
            disease_by_DOID[item_DOID].append(match.group(1).strip())
            continue
        if line.startswith('synonym:'):
            match = re.match('^synonym: \"(.*)\".*', line)
            disease_by_DOID[item_DOID].append(match.group(1).strip())
            continue

diseases = {} # key - disease name; value - DOID
for DOID in disease_by_DOID:
    for disease in disease_by_DOID[DOID]:
        diseases[disease] = DOID
        if disease[0].islower():
            diseases[disease[0].upper() + disease[1:]] = DOID


root = WTreeNode()

# строим дерево с названиями всех болезней
for disease in diseases.keys():
    disease_list = disease.split()
    cur_node = root
    for i, word in enumerate(disease_list):
        if not(word in cur_node.children):
            cur_node.children[word] = WTreeNode()
        cur_node = cur_node.children[word]
        if i == len(disease_list) - 1:
            cur_node.is_end = True