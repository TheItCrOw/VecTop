from vectop import vectop
import os
import psycopg
import uuid
import time

root = os.getcwd()
example = '''
Sie wollen jetzt, um das Gasproblem im kommenden Winter zu lösen, bei den Lieferanten umschichten, was dem Ministerium zum Teil auch gelingen wird, aber natürlich verbunden mit entsprechend hohen Kosten für die Verbraucherinnen und Verbraucher und für die Wirtschaft in Deutschland. Dazu einige Zahlen: Im Jahr 2021, im letzten Jahr, haben die sechs verbliebenen deutschen Kernkraftwerksblöcke in acht von zwölf Monaten mehr Strom erzeugt als sämtliche circa 1,5 Millionen Photovoltaikanlagen in Deutschland zusammen. Während wir bei Kernkraftwerken über real existierende Anlagen sprechen, die ich besichtigen und begehen kann, bei denen ich schauen kann, wo der Treibstoff reinkommt, damit es funktioniert,haben Sie beim Wasserstoff nichts. Zum anderen ist jetzt der Zeitpunkt gekommen, an dem wir über die sichere, zuverlässige und auch bezahlbare Energieversorgung des Landes in den kommenden Jahren und Wintern reden müssen
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
    topics = v.extract_topics(example, 'de-DE')
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
    extract_from_many(v)
