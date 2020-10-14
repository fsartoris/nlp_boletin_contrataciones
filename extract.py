import json
import time
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from libs.common import html_cleaner
from libs.storage import persist_json


def parse(url, date):
    parse_contrataciones(url, date)


def parse_contrataciones(base_url, fecha):
    seccion = 'tercera'
    rubro = 1711
    return parse_page(base_url, seccion, fecha, rubro)


def request_with_headers(url):
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    return requests.get(url, headers=headers)


def parse_page_item(url):

    response = request_with_headers(url)
    soup = BeautifulSoup(response.content, 'lxml')
    #title = soup.title.get_text()

    content = soup.find(id="detalleAviso")
    body = ""

    if content != None:
        article = soup.find(id="detalleAviso").find(
            id="cuerpoDetalleAviso").findAll("p")

        for p in article:
            body = "%s%s " % (body, html_cleaner(p.get_text()))

    return body


def parse_page(url, seccion, fecha, rubro):

    scrap_url = "%s/seccion/%s/%s?rubro=%s" % (url, seccion, fecha, rubro)
    response = request_with_headers(scrap_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    content = soup.find(id="avisosSeccionDiv")

    if content == None:
        return

    row = content.findAll("div", {"class": "row"})

    if row != None:
        array_content = str(row).split(',')
    else:
        array_content = None

    url_to_parse = list()

    for item_content in array_content:
        if(item_content.find("href") != -1):
            link = BeautifulSoup(item_content, "lxml").find_all('a', href=True)
            href = "%s%s" % (url, link[0].get('href'))
            url_to_parse.append(href)

    response = {}

    for u in url_to_parse:
        if(u.find("anexos") == -1):
            body = parse_page_item(u)
            persist_json(u, body, fecha)
            response[u] = body
            time.sleep(2)

    return response
