import re
import string
from stop_words import get_stop_words


def html_cleaner(text):
    clean = re.compile('{.*?}')
    text = re.sub(clean, '', text)
    return str(re.sub("table tr td", '', text)).strip()


def text_cleaner(text, stopwords=None):

    text = ''.join([i for i in text if not i.isdigit()])
    punct = string.punctuation + '”' + '´' + '—'
    translator = str.maketrans('', '', punct)
    return text.translate(translator).strip()


def remove_stopwords(text, stop_words_customized):
    custom_stopword = get_stop_words('spanish') + stop_words_customized
    return ' '.join([word for word in text.split() if word not in custom_stopword])


def format_money(m):
    return '$ {:,.2f}'.format(m).replace(",", "@").replace(".", ",").replace("@", ".")
