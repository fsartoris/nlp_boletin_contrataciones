import json
import spacy
import load

from libs.nlp import parse_money
from libs.nlp import parse_business
from libs.storage import get_files
from libs.storage import get_file_content

from model.Company import Company
from database.dbo import check_padron

def process(fecha):

    response = []

    nlp_spacy = spacy.load("es_core_news_md")

    for filename in get_files(fecha):
        json_parsed = get_file_content(fecha, filename)
        print(json_parsed)

        url = json_parsed['url']
        money = parse_money(json_parsed['body'])
        business = parse_business(nlp_spacy, json_parsed['body'])

        for bus in business:
            bus = bus.replace(u'\xa0', u' ').replace(" ", "").strip()
            result = check_padron(bus)
            if result == None:
                idx = 1
                length = len(bus)
                while result == None and idx < int(length):
                    result = check_padron(bus[idx:length].strip())
                    idx += 1

            if not result is None:
                response.append(Company(result[0], result[1], money, url))

    return response
