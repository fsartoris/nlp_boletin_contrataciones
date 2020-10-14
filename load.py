from api.twitter import compose_tweet
from database.dbo import insert_parsed


def process(array):
    for company in array:
        insert_parsed(company.cuit, company.razon, company.money, company.url)
        compose_tweet(company.razon, company.money, company.url)
