from datetime import date, timedelta
import psycopg
import time
import numpy as np
import pytextrank
from pgvector.psycopg import register_vector
# https://pypi.org/project/spiegel-scraper/
import json
from chatgpt import chatgpt_api
from spiegel_online import spiegel_api
from translate import translator
import spacy

connection_string = ''
sentenced_table = 'spiegel_embeddings'
summarized_table = 'spiegel_embeddings_summarized'
summarized_table_eng = 'spiegel_embeddings_summarized_eng'
nlp = spacy.load('de_core_news_sm')
nlp.add_pipe("textrank")


ger_eng_channels = {
    # channels
    'Ausland': 'Foreign Countries',
    'Backstage': 'Backstage',
    'Community': 'Community',
    'Familie': 'Family',
    'Fitness': 'Fitness',
    'Geschichte': 'History',
    'Gesundheit': 'Health',
    'International': 'International',
    'Job & Karriere': 'Jobs & Career',
    'Kultur': 'Culture',
    'Mobilität': 'Mobility',
    'Netzwelt': 'Network World',
    'Panorama': 'Panorama',
    'Partnerschaft': 'Partnership',
    'Politik': 'Politics',
    'Psychologie': 'Psychology',
    'Reise': 'Travel',
    'Services': 'Services',
    'Sport': 'Sport',
    'Start': 'Start',
    'Stil': 'Style',
    'Tests': 'Tests',
    'Wirtschaft': 'Economy',
    'Wissenschaft': 'Science',

    # subchannels
    'American Football': 'American Football',
    'Anzeige': 'Advertisement',
    'Apps': 'Apps',
    'Auto-Zubehör': 'Cars',
    'Basketball': 'Basketball',
    'BeyondTomorrow': 'BeyondTomorrow',
    'Bildung': 'Education',
    'Brettspiele': 'Board Games',
    'Business': 'Business',
    'Camping': 'Camping',
    'default': 'default',
    'Deutschland': 'Germany',
    'Diagnose': 'Diagnose',
    'Diagnose & Therapie': 'Diagnose & Therapy',
    'Eishockey': 'Ice Hockey',
    'Elektronik': 'Electronics',
    'Elterncouch': 'Parents',
    'Ernährung & Fitness': 'Nutritions & Fitness',
    'Europa': 'Europe',
    'Europe': 'Europe',
    'Fahrbericht': 'Driving Report',
    'Fahrkultur': 'Driving Culture',
    'Fahrrad & Zubehör': 'Bicycle & Accessories',
    'Fernweh': 'Wanderlust',
    'Formel 1': 'Formula 1',
    'Formel1': 'Formula 1',
    'Fußball-News': 'Soccer News',
    'Gadgets': 'Gadgets',
    'Games': 'Games',
    'Garten': 'Garden',
    'Germany': 'Germany',
    'Gesellschaft': 'Society',
    'Golf': 'Golf',
    'Handball': 'Handball',
    'Haushalt': 'Household',
    'Justiz': 'Law',
    'Justiz & Kriminalität': 'Law & Order',
    'Kino': 'Cinema',
    'Küche': 'Kitchen',
    'Leute': 'People',
    'Ligue 1': 'Ligue 1',
    'Literatur': 'Literature',
    'Medizin': 'Medicine',
    'Mensch': 'Human',
    'Musik': 'Music',
    'Natur': 'Nature',
    'Netzpolitik': 'Network Politics',
    'Olympia': 'Olympics',
    'Premier League': 'Premier League',
    'Primera Division': 'Primera Division',
    'Psychologie': 'Psychology',
    'S-Magazin': 'default',
    'Schwangerschaft & Kind': 'Pregnancy & Children',
    'Serie A': 'Seria A',
    'Sex': 'Sex',
    'Sex & Partnerschaft': 'Sex & Partnership',
    'Soziales': 'Social',
    'Staat & Soziales': 'State & Social',
    'Städte': 'Cities',
    'Städtereisen': 'City Travelling',
    'Technik': 'Technology',
    'Tennis': 'Tennis',
    'Tests': 'Tests',
    'Tomorrow': 'Tomorrow',
    'TV': 'TV',
    'Unternehmen': 'Companies',
    'Unternehmen & Märkte': 'Companies & Markets',
    'Verbraucher & Service': 'Consumers & Service',
    'Web': 'Web',
    'Weltall': 'Space',
    'Wintersport': 'Winter Sports',
    'World': 'World',
    'Zeitgeist': 'Current Mindset',
    'Zeitzeugen': 'Time Witness'
}


def write_to_json_file(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def insert_spiegel_embedding(item, table):
    with psycopg.connect(connection_string) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO " + table +
                " (content, headline_main, headline_social, breadcrumbs, url, channel, subchannel, intro, topics, embedding, article_id, \"order\")" + 
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (item['content'],
                 item['headline_main'],
                 item['headline_social'],
                 item['breadcrumbs'],
                 item['url'],
                 item['channel'],
                 item['subchannel'],
                 item['intro'],
                 item['topics'],
                 item['embedding'],
                 item['article_id'],
                 item['order']
                 ))
            conn.commit()


def insert_spiegel_embedding_eng(item, table):
    with psycopg.connect(connection_string) as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO " + table +
                " (content, url, channel, subchannel, embedding, article_id)" + 
                " VALUES (%s, %s, %s, %s, %s, %s)",
                (item['content'],
                 item['url'],
                 item['channel'],
                 item['subchannel'],
                 item['embedding'],
                 item['article_id'],
                 ))
            conn.commit()


def get_labeled_speeches():
    with psycopg.connect(connection_string) as conn:
        return conn.execute('SELECT * FROM labeled_speeches').fetchall()


def get_connection_string():
    with open('pg_connection_string.txt', 'r') as f:
        return f.read()


def get_openai_api_key():
    with open('openai_api_key.txt', 'r') as f:
        return f.read()


def tr_summarize(text, top):
    ''' summarizes the text with text rank'''
    doc = nlp(text)
    summary = ''
    # Create the summary
    for sentence in doc._.textrank.summary(limit_sentences=top):
        summary = summary + str(sentence) + ' '
    return summary.replace('\n', ' ').replace('\r', ' ')


def generate_spiegel_embeddings_summarized(date):
    '''Generates the word embeddings on basis of summary'''
    api = spiegel_api()
    embedder = chatgpt_api(get_openai_api_key())
    print("Currently doing summarized: ")
    print(start_date)
    articles = []
    try:
        articles = api.get_articles_of_date(date)
    except Exception as ex:
        print("Error while fetching spiegel articles:")
        print(ex)
        print("Waiting a few seconds, this is probably due to timeout.")
        time.sleep(60)
        generate_spiegel_embeddings_summarized(date)

    for article in articles:
        summary = tr_summarize(article['text'], 5)
        embeddings = []
        if(len(summary) < 10):
            continue
        try:
            embeddings = embedder.embed(summary)
        except Exception as ex:
            print("Error while fetching embedding text:")
            print(ex)
            print("Waiting a few seconds, this is probably due to timeout.")
            time.sleep(600)
            generate_spiegel_embeddings_summarized(date)
        item = {
            'content': summary,
            'headline_main': article['headline']['main'],
            'headline_social': article['headline']['social'],
            'breadcrumbs': article['breadcrumbs'],
            'url': article['url'],
            'channel': article['channel'],
            'subchannel': article['subchannel'],
            'intro': article['intro'],
            'topics': article['topics'],
            'embedding': embeddings,
            'article_id': article['id'],
            'order': 1
        }
        insert_spiegel_embedding(item, summarized_table)


def generate_spiegel_embeddings_sentenced(date):
    '''Generates the embeddings on basis of sentences'''
    api = spiegel_api()
    embedder = chatgpt_api(get_openai_api_key())
    print("Currently doing sentenced: ")
    print(start_date)
    articles = []
    try:
        articles = api.get_articles_of_date(date)
    except Exception as ex:
        print("Error while fetching spiegel articles:")
        print(ex)
        print("Waiting a few seconds, this is probably due to timeout.")
        time.sleep(600)
        generate_spiegel_embeddings_sentenced(date)

    for article in articles:
        sentences = [i for i in nlp(article['text']).sents]
        # We want to embed each sentence
        embeddings = []
        c = 0
        for sent in sentences:
            try:
                embeddings = embedder.embed(str(sent))
            except Exception as ex:
                print("Error while fetching embedding text:")
                print(ex)
                print("Waiting a few seconds, this is probably due to timeout.")
                time.sleep(60)
                generate_spiegel_embeddings_sentenced(date)
            item = {
                'content': str(sent),
                'headline_main': article['headline']['main'],
                'headline_social': article['headline']['social'],
                'breadcrumbs': article['breadcrumbs'],
                'url': article['url'],
                'channel': article['channel'],
                'subchannel': article['subchannel'],
                'intro': article['intro'],
                'topics': article['topics'],
                'embedding': embeddings,
                'article_id': article['id'],
                'order': c
            }
            insert_spiegel_embedding(item, sentenced_table)
            c = c + 1


def check_test_sentenced():
    speeches = get_labeled_speeches()
    results = []
    embedder = chatgpt_api(get_openai_api_key())

    for s in speeches:
        top_topics = []
        sub_topics = []
        topics = []
        speech = s[0]
        print("==========================")
        print(speech)

        sentences = [i for i in nlp(speech).sents]
        for sent in sentences:
            embedding = np.array(embedder.embed(str(sent)))
            with psycopg.connect(connection_string) as conn:
                register_vector(conn)
                sim = conn.execute('SELECT * FROM ' + sentenced_table + ' ORDER BY embedding <=> %s LIMIT 5', (embedding,)).fetchall() 
                # print(sim)
                top_topics.append(sim[0][6])
                sub_topics.append(sim[0][7])
                topics.append(sim[0][9])

        print("==========================")
        print(top_topics)
        print(sub_topics)
        print(topics)
        print("==========================\n\n")


def check_test_summarized():
    speeches = get_labeled_speeches()
    results = []
    embedder = chatgpt_api(get_openai_api_key())
    for s in speeches:
        content = s[1]
        top_topics = []
        sub_topics = []
        topics = []
        if(content == ''):
            continue
        print("=================== \n")
        print(str(content))
        print("=================== \n")
        embedding = np.array(embedder.embed(str(content)))
        with psycopg.connect(connection_string) as conn:
            register_vector(conn)
            sim = conn.execute('SELECT * FROM ' + summarized_table + ' ORDER BY embedding <=> %s LIMIT 5', (embedding,)).fetchall() 
            #print(sim)
            for vec in sim:
                top_topics.append(vec[5])
                sub_topics.append(vec[6])
                topics.append(vec[3])
        print("==========================\n")

        print(top_topics)
        print(sub_topics)
        print(topics)
        print("==========================\n\n\n")
        result = {
            'full_speech': s[0],
            'summary': content,
            'target_topic': s[2],
            'pred_channel': top_topics,
            'pred_subchannel': sub_topics,
            'pred_topics': topics
        }
        results.append(result)
    write_to_json_file('speeches_pred_4k.json', results)


def generate_spiegel_embeddings_summarized_eng(trans, offset, limit):
    '''
    Here we dont fetch the articles from spiegel again. We use already
    fetched articles in the database and translate and embed them again.
    '''
    embedder = chatgpt_api(get_openai_api_key())

    def handle_one(r):
        eng = trans.translate_german_to_english(r[0])
        channel = ger_eng_channels[r[5]] if r[5] in ger_eng_channels else r[5]
        subchannel = ger_eng_channels[r[6]] if r[6] in ger_eng_channels else r[6]

        try:
            embeddings = embedder.embed(eng)
        except Exception as ex:
            print("Error in embedding, prolly timeout. Waiting then retrying")
            time.sleep(120)
            handle_one(r)

        insert_spiegel_embedding_eng({
            'content': eng,
            'url': r[4],
            'channel': channel,
            'subchannel': subchannel,
            'embedding': embeddings,
            'article_id': r[9]
        }, summarized_table_eng)

    with psycopg.connect(connection_string) as conn:
        result = conn.execute(
            'SELECT content, headline_main, headline_social, breadcrumbs, url, channel, subchannel, intro, topics, article_id FROM ' + summarized_table + ' OFFSET ' + str(offset) + ' LIMIT ' + str(limit)).fetchall()
        for r in result:
            handle_one(r)

    print('Done with offset ' + str(offset) + ' and limit ' + str(limit))


if __name__ == "__main__":
    connection_string = get_connection_string()
    # trans = translator()
    # limit = 25
    # for i in range(1001, 99999999, limit):
    #    generate_spiegel_embeddings_summarized_eng(trans, i, limit)

    # check_test_summarized()

    start_date = date(2016, 11, 19)
    end_date = date(2000, 1, 1)
    delta = timedelta(days=1)
    while start_date >= end_date:
        try:
            generate_spiegel_embeddings_summarized(start_date)
            start_date -= delta
        except Exception as ex:
            print("Unknown error. Restarting in a bit.")
            time.sleep(60)
