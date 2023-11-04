import json
import os
import psycopg
# Just a utility class to put some speeches into the postgres db.


def get_connection_string():
    with open('pg_connection_string.txt', 'r') as f:
        return f.read()


def insert_speech(text, summary, topic, subtopic):
    with psycopg.connect(get_connection_string()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO " + 'labeled_speeches' +
                " (full_speech, extractive_summary, topic, subtopic)" + 
                " VALUES (%s, %s, %s, %s)",
                (text,
                 summary,
                 topic,
                 subtopic,
                 ))
            conn.commit()


def main():
    root = "E:\\Python_Projects\\TopicExtracter\\src\\spiegel_embedder\\testing\\speeches\\"
    for filename in os.listdir(root):
        prot = ''
        with open(root + filename, 'r', encoding='utf-8') as f:
            prot = json.load(f)
        print(prot)
        agenda_items = prot['AgendaItems']
        for speech in prot['NLPSpeeches']:
            text = speech['Text'].replace('\n', '')
            if (len(text) < 5):
                continue
            summary = speech['ExtractiveSummary']
            agenda = agenda_items[speech['AgendaItemNumber'] - 1]['Title']
            print(text)
            print(summary)
            print(agenda)
            print('\n\n')
            insert_speech(text, summary, agenda, '')


main()
