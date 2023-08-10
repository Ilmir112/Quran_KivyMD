import json


def data_from_json(ayat):
    with open("data/data.json/sur_30.json", "r", encoding='utf-8') as file:
        data = json.load(file)
    dict_ques = {}
    verse_key = 1
    for i in range(1, len(data['verses']) + 1):
        verse_key += 1
        for j in data['verses'][i - 1]['words']:
            if j['audio_url'] != None:
                dict_ques.setdefault(i, []).append([j["text"], j['audio_url'], j['translation']['text'], j["transliteration"]['text']])


    return dict_ques
