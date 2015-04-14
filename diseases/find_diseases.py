__author__ = 'yarygin_konstantin'

import disease_list_processing as dlp


def find_diseases(text):
    text = text.split()
    text = map(lambda x: x.strip('.,'), text)
    diseases_in_text = []
    for i, word in enumerate(text):
        if word in dlp.root.children:
            cur_node = dlp.root.children[word]
            flag = True
            j = i
            while flag:
                if j >= len(text) - 1:
                    break
                j += 1
                flag = False
                if cur_node.is_end:
                    diseases_in_text.append(text[i:j])
                if text[j] in cur_node.children:
                    cur_node = cur_node.children[text[j]]
                    flag = True

    diseases_in_text = map(lambda x: ' '.join(x), diseases_in_text)
    DOIDs_list = map(lambda x: dlp.diseases[x], diseases_in_text)
    disease_ids = list(set(DOIDs_list))
    disease_names = map(lambda x: dlp.disease_by_DOID[x][0], disease_ids)
    disease_ids_dict = {disease_id: 0 for disease_id in disease_ids}
    for disease_id in DOIDs_list:
        disease_ids_dict[disease_id] += 1
    return disease_ids_dict, disease_names
