import re

from libs.common import text_cleaner
from libs.common import format_money
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher


def parse_money(text):

    money_amt = 0
    money_regex = re.compile(r'(\d{1,3}(?:.\d{3})*(?:\.\d+))')

    for m in money_regex.finditer(text):
        if text[m.start()-2:m.end()][0] == "$":
            money_str = text[m.start():m.end()]
            money_amt += float(money_str.replace(".",
                                                 '').replace(",", '').replace(' ', ''))

    if(money_amt == 0):
        return "N/D"
    else:
        return format_money(money_amt)


def parse_business(nlp_spacy, text):

    matcher = Matcher(nlp_spacy.vocab)

    pattern1 = [{'LOWER': 'sa'}]
    pattern2 = [{'LOWER': 'sas'}]
    pattern3 = [{'LOWER': 'srl'}]
    pattern4 = [{'LOWER': 'saas'}]
    pattern5 = [{'LOWER': 'saci'}]

    matcher.add('business_names', None, pattern1,
                pattern2, pattern3, pattern4, pattern5)

    token_offset = 5

    text = nlp_spacy(text_cleaner(text.lower()))
    found_matches = matcher(text)

    business_list = []

    for match_id, start, end in found_matches:
        span = text[(start - token_offset):end]
        business_list.append(span.text)

    return list(dict.fromkeys(business_list))
