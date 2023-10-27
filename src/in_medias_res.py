from vectop import vectop
import os
import psycopg
import uuid
import time

root = os.getcwd()
example_text = '''
Deutschland hat seit 2022 einen Wachstumsnachlass von 1,5%, die Schulden werden immer größer.
'''


def get_connection_string():
    with open('./spiegel_embedder/pg_connection_string.txt', 'r') as f:
        return f.read()


def get_openai_api_key():
    with open('./spiegel_embedder/openai_api_key.txt', 'r') as f:
        return f.read()


def get_labeled_speeches(offset):
    with psycopg.connect(get_connection_string()) as conn:
        return conn.execute('SELECT * FROM labeled_speeches' + ' OFFSET ' + str(offset)).fetchall()


def example(v):
    '''A simple example of vectop for one text'''
    topics = v.extract_topics(example_text, 'de-DE')
    print(topics)


def extract_from_many(v):
    '''
    Extracts from many and stores it in the vectop database for
    further evaluation. Can be used to evalute the database on ur texts
    '''
    datasets = get_labeled_speeches(0)
    with psycopg.connect(get_connection_string()) as conn:
        with conn.cursor() as cur:
            for d in datasets:
                print('Doing: ')
                print(d)
                print('\n\n')
                tid = str(uuid.uuid4())
                try:
                    topics = v.extract_topics(d[0], 'de-DE')
                except Exception as ex:
                    print("Timeout or other error. Retry")
                    print(ex)
                    time.sleep(60)
                    continue
                for topic in topics:
                    for sub_topic in topic[1]:
                        cur.execute(
                            "INSERT INTO " + 'predicted_topics' +
                            " (pred_topic, pred_subtopic, summary, full_text, tid)" + 
                            " VALUES (%s, %s, %s, %s, %s)",
                            (topic[0],
                             sub_topic,
                             d[1],
                             d[0],
                             tid
                             ))
                        conn.commit()


if __name__ == "__main__":
    v = vectop(get_openai_api_key(), get_connection_string())
    print("Loaded VecTop module")
    example(v)
