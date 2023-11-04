from chatgpt import chatgpt_api
import psycopg
import random
import os
import json


cls = lambda: os.system('cls')
chat_gpt = {}

german_prompt = '''
Es sind ein Text und zwei Kategorien gegeben. Antworte "ok", wenn der Text zu den Kategorien passt. Ansonsten antworte mit "no". Antworte nicht im ganzen Satz! Nur "ok" oder "no"!

### TEXT
[TEXT]

### Kategorien
[TOPICS]

'''


def get_connection_string():
    with open('pg_connection_string.txt', 'r') as f:
        return f.read()


def get_openai_api_key():
    with open('openai_api_key.txt', 'r') as f:
        return f.read()


def load_labeled_speeches_json():
    with open("E:\\Python_Projects\\TopicExtracter\\src\\spiegel_embedder\\testing\\speeches_pred_4k.json", encoding='utf-8') as f:
        return json.loads(f.read())


def load_predicted_topics_db():
    with psycopg.connect(get_connection_string()) as conn:
        return conn.execute('SELECT * FROM predicted_topics WHERE topic_correct IS NULL ORDER BY id ASC').fetchall()


def insert_evaluation(full_text,
                      summary,
                      pred_topic,
                      pred_sub_topic,
                      pred_breadcrumbs,
                      target_agenda,
                      correct):
    with psycopg.connect(get_connection_string()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO " + 'evaluation' +
                " (full_text, summary, pred_topic, pred_sub_topic, pred_breadcrumbs, target_agenda, correct)" + 
                " VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (full_text,
                 summary,
                 pred_topic,
                 pred_sub_topic,
                 pred_breadcrumbs,
                 target_agenda,
                 correct
                 ))
            conn.commit()


def evaluate_with_chatgpt(text, topic, subtopic):
    # Asks chatgpt whether the given text suits the topic and subtopic
    topics = [topic]
    if(subtopic != 'default' and subtopic != ''):
        topics.append(subtopic)
    prompt = german_prompt.replace('[TEXT]', text).replace('[TOPICS]', ', '.join(topics))
    print(prompt)
    return chat_gpt.get_response(prompt)


def evaulate_datasets_automatically(datasets):
    # Evaluates a bunch of labeled datasets
    for d in random.sample(datasets, 100):
        topic = d['pred_channel'][0]
        sub_topic = d['pred_subchannel'][0]

        print("Doing eval for text: ")
        evaluate = evaluate_with_chatgpt(d['summary'], topic, sub_topic)
        correct = 'ok' in evaluate
        insert_evaluation(d['full_speech'], d['summary'], topic,
                          sub_topic, d['pred_topics'],
                          d['target_topic'], correct)
        print('\n Result: ' + evaluate + '\n\n')


def evaluate_datasets_manually(datasets):
    with psycopg.connect(get_connection_string()) as conn:
        for d in datasets:
            cls()
            print("===== A new prediction =====\n")
            print("id: " + str(d[7]))
            print(d[3])
            print("\n===== Topic: =====")
            print(d[0])
            print("Ok? Type 1, else 2")
            inp = int(input())
            conn.execute('UPDATE predicted_topics SET topic_correct = ' + str(inp == 1) + ' where id = ' + str(d[7]))
            conn.commit()
            print("\n===== Subtopic: =====")
            print(d[1])
            inp = int(input())
            print("Ok? Type 1, else 2")
            conn.execute('UPDATE predicted_topics SET subtopic_correct = ' + str(inp == 1) + ' where id = ' + str(d[7]))
            conn.commit()


if __name__ == "__main__":
    chat_gpt = chatgpt_api(get_openai_api_key())

    datasets = load_predicted_topics_db()
    evaluate_datasets_manually(datasets)
