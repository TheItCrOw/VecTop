import json
import time
import psycopg
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from pgvector.psycopg import register_vector
from chatgpt import chatgpt_api
from ny_times import times_api

connection_string = ''
start_date = date(2020, 5, 27)
end_date = date(2000, 1, 1)


def get_connection_string():
    with open('pg_connection_string.txt', 'r') as f:
        return f.read()


def get_openai_api_key():
    with open('openai_api_key.txt', 'r') as f:
        return f.read()


def get_times_api_key():
    with open('times_api_key.txt', 'r') as f:
        return f.read()


def insert_times_embedding(content,
                           headline,
                           breadcrumbs,
                           url,
                           channel,
                           subchannel,
                           intro,
                           abstract,
                           snippet,
                           embedding_vector,
                           article_id):
    with psycopg.connect(connection_string) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO " + 'times_embeddings' +
                " (content, headline, breadcrumbs, url, channel, subchannel, intro, abstract, snippet, embedding, article_id)" + 
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (content,
                 headline,
                 breadcrumbs,
                 url,
                 channel,
                 subchannel,
                 intro,
                 abstract,
                 snippet,
                 embedding_vector,
                 article_id
                 ))
            conn.commit()


def generate_times_embeddings(year, month):
    '''Fetches time articles and creates embeddings from them'''
    print("Doing " + str(month) + "/" + str(year))
    api = times_api(get_times_api_key())
    embedder = chatgpt_api(get_openai_api_key())
    articles = []
    try:
        articles = api.get_articles_of_date(year, month)
        print("Found: " + str(len(articles)) + " articles")
    except Exception as ex:
        print("Error while fetching articles, maybe a timeout. Retrying soon")
        print(ex)
        time.sleep(120)
        generate_times_embeddings(year, month)

    for article in articles:
        # The full text is not provided within the api. I could scrape it, but 
        # chances are there will be html, other tags or missing words in it.
        # For now: lets test with just the headline, abstract and first para
        text = article['abstract'] + ' ' + article['lead_paragraph']
        if(text == ''):
            continue
        embeddings = []
        try:
            embeddings = embedder.embed(text)
        except Exception as ex:
            print("Error while fetching embedding text:")
            print(ex)
            print("Waiting a few seconds, this is probably due to timeout.")
            time.sleep(300)
            start_date -= relativedelta(months=+1)
            generate_times_embeddings(start_date.year, start_date.month)

        # Now store the relevant data in the database
        try:
            breadcrumbs = list(map(lambda k: k['value'], article['keywords']))
            insert_times_embedding(text,
                                   article['headline']['main'],
                                   breadcrumbs,
                                   article['web_url'],
                                   article['keywords'][0]['value'],
                                   article['keywords'][1]['value'],
                                   article['lead_paragraph'],
                                   article['abstract'],
                                   article['snippet'],
                                   embeddings,
                                   article['_id'])
        except Exception as ex:
            # Dont print it. There are too many.
            # print("Failed to insert one article, prolly missing channels. Skipping it.")
            # print(ex)
            pass


if __name__ == "__main__":
    connection_string = get_connection_string()
    while start_date >= end_date:
        try:
            generate_times_embeddings(start_date.year, start_date.month)
            start_date -= relativedelta(months=+1)
        except Exception as ex:
            print("Unknown error. Restarting in a bit.")
            time.sleep(60)
