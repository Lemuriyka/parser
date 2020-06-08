#!/usr/bin/python3

import sys
import getopt

from bs4 import BeautifulSoup


BASE_SEARCH_ID = "make-everything-ok-button"


# Totally excessive but PyDictionary and Vocabulary are not supported anymore
def synonyms(term):
    from itertools import chain
    from nltk.corpus import wordnet

    synonyms = wordnet.synsets(term)
    lemmas = list(set(chain.from_iterable([word.lemma_names() for word in synonyms])))
    return lemmas


def calc_text_match(source_text, target_text):
    source_set = source_text.strip().replace('-', ' ').split()
    source_pool = []

    for word in source_set:
        source_pool.append(word.lower())
        source_pool += synonyms(word)

    target_set = target_text.strip().replace('-', ' ').split()
    match_score = 0
    for word in target_set:
        if word.lower() in source_pool:
            match_score += 25/len(target_set)

    return match_score


def main(argv):
    if len(argv) < 2:
        print('Two pages locations should be provided')
        return
    
    source_file = argv[0]
    target_file = argv[1]

    _id = BASE_SEARCH_ID
    if len(argv) == 3:
        _id = argv[2]

    score_coef = {
        'class': 25,
        'href': 25,
        'title': 25,
        'text': 25
    }

    with open(source_file, 'r') as sf:
        soup = BeautifulSoup(sf, 'lxml')
        source = soup.find(id=_id)
        source_data = source.attrs

    with open(target_file, 'r') as tf:
        soup = BeautifulSoup(tf, 'lxml')
        search_data = soup.find_all(source.name)

    result_set = []
    for item in search_data:
        score = {
            'class': 0,
            'href': 0,
            'title': 0,
            'text': 0
        }
        item_data = item.attrs

        if item_data.get('class') == source_data.get('class'):
            score['class'] = score_coef['class']

        if source_data.get('href').strip('#') in item_data.get('href'):
            score['href'] = score_coef['href']

        if all((source_data.get('title'), item_data.get('title'))):
            score['title'] = calc_text_match(source_data.get('title'), item_data.get('title'))

        if all((source.string, item.string)):
            score['text'] = calc_text_match(source.string, item.string)

        score['general'] = sum(score.values())
        if score['general'] >= 50:
            score['item'] = item
            result_set.append(score)

    max_score = max([obj['general'] for obj in result_set])
    result = [obj for obj in result_set if obj['general'] == max_score]
    if len(result) != 1:
        print('Sorry, search was not successful')
        return
    print('Result element is: ', result[0]['item'])
    print("""
    Summary:
    General match score: {}%,
    element class match contribution: {}%,
    element href match contribution: {}%,
    element title match contribution: {}%,
    element text match contribution: {}%
    """.format(max_score, result[0]['class'], result[0]['href'], result[0]['title'], result[0]['text']))
    # print(result[0])


if __name__ == '__main__':
    main(sys.argv[1:])
