# -*- coding: UTF-8 -*-

headers = ['organism_name',
           'strain',
           'species',
           'genus',
           'family',
           'order',
           'class',
           'phylum',
           'kingdom']



with open('bacteria/taxonomy_table_filtered.tsv') as f:
    f.readline()
    data = f.readlines()
data = map(lambda x: x.strip('\n').split('\t'), data)


taxon_names = {}
full_species = {}
# заносим в full_species всевозможные имена для каждого таксономического уровня
for i, taxon in enumerate(headers):
    taxon_names[taxon] = {}
    for taxon_line in data:
        if taxon == 'species':
            name = taxon_line[i].split(' ', 1)[1]
            full_species[name] = taxon_line[i]
        else:
            name = taxon_line[i]
        taxon_names[taxon][name] = 0
    if 'NA' in taxon_names[taxon]:
        del taxon_names[taxon]['NA']
