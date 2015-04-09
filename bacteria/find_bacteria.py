# -*- coding: UTF-8 -*-

import bacteria_list_processing as blp

headers = [
    # 'organism_name',
    # 'strain',
    # 'species',
    'genus',
    # 'family',
    # 'order',
    # 'class',
    # 'phylum',
    # 'kingdom'
]


def find_bacteria(abstract):
    ret = {}
    bacteria_in_text = []
    # print abstract
    text = abstract.split()
    # print text
    text = map(lambda x: x.strip('1234567890*()[]-.,? \'\"'), text)
    # print text
    text = filter(lambda x: len(x) > 1, text)
    # print text
    # text = filter(lambda x: x.isalpha(), text)
    # text = map(lambda x: x.lower(), text)

    for word in text:
        for taxon in headers:
            if word in blp.taxon_names[taxon]:
                # Полное название вида имеет вид 'Род вид', например 'Bacteroides fragilis'
                # В этом случае ищем только второе слово
                if taxon == 'species':
                    bacteria_in_text.append((taxon, blp.full_species[word]))
                else:
                    bacteria_in_text.append((taxon, word))
    ret = {}

    for taxon, name in bacteria_in_text:
        if not (taxon in ret):
            ret[taxon] = {}
        if not (name in ret[taxon]):
            ret[taxon][name] = 0
        ret[taxon][name] += 1

    for taxon in ret:
        ret[taxon] = sorted(ret[taxon].items(),
                            key=lambda x: x[1], reverse=True)

    ret = ret.items()

    return ret