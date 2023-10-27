import psycopg
import pytextrank
from pgvector.psycopg import register_vector
import spacy
import openai
import numpy as np


class vectop:

    def __init__(self, openai_api_key, connection_string):
        self.nlp = spacy.load('de_core_news_sm')
        self.nlp.add_pipe("textrank")

        self.max_sent = 5
        openai.api_key = openai_api_key
        self.connection_string = connection_string

    def embed(self, text):
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embeddings = response['data'][0]['embedding']
        return embeddings

    def tr_summarize(self, text, top):
        ''' summarizes the text with text rank'''
        doc = self.nlp(text)
        summary = ''
        # Create the summary
        for sentence in doc._.textrank.summary(limit_sentences=top):
            summary = summary + str(sentence) + ' '
        return summary.replace('\n', ' ').replace('\r', ' ')

    def get_sim(self, vec, sim_table):
        with psycopg.connect(self.connection_string) as conn:
            register_vector(conn)
            sim = conn.execute('SELECT * FROM ' + sim_table + ' ORDER BY embedding <=> %s LIMIT 5', (vec,)).fetchall() 
            return sim

    def extract_topics(self, text, language):
        '''Extract topics from a given text'''
        # Language code by: http://www.lingoes.net/en/translator/langcode.htm
        if(language != 'de-DE'):
            raise Exception("Currently, only the German language is supported")

        # First step is too check how long the text is. If it exceeds a
        # threshold of X sentences, summarize it.
        sentences = [str(i) for i in self.nlp(text).sents]
        final = ' '.join(sentences)  # This is the text we will extract from
        if(len(sentences) > self.max_sent):
            final = self.tr_summarize(text, self.max_sent)

        # Make the embeddings
        embedded = np.array(self.embed(final.strip()))
        sim = self.get_sim(embedded, 'spiegel_embeddings_summarized')

        # Extract the relevant topics
        tops = {}
        sub_tops = {}
        c = 0
        for vec in sim:
            # Index 5: main_topic, index 6: sub_topic, index 3: breadcrumbs
            t = vec[5]
            st = vec[6]

            # We always take the nearest embedding
            if(c == 0):
                tops[t] = 2
                sub_tops[t] = [st]
                c += 1
                continue
            # For the rest we count the occurences and track the subtopics
            if t in tops:
                tops[t] = tops[t] + 1
                li = sub_tops[t]
                li.append(st)
            else:
                tops[t] = 1
                sub_tops[t] = [st]
            c += 1

        # We want only those topics with at least 2 occurences
        final_topics = []
        for k, v in tops.items():
            if(v >= 2):
                final_topics.append([k, list(set([i for i in sub_tops[k] if i != 'default']))])
        return final_topics
