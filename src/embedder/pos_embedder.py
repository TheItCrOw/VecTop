import spacy
import numpy as np

# https://www.sketchengine.eu/german-stts-part-of-speech-tagset/
german_pos_tags = [
    'ADJA',     # Adjective
    'ADJD',     # Adjective comparative
    'ADV',      # adverb

    # Everything noun related
    'NA',       # Noun
    'NN',       # Noun Proper singular
    'NE',       # Adjverb... dont know about this one

    # All form of verbs
    'VAIMP',
    'VAINF',
    'VAPP',
    'VMFIN',
    'VMINF',
    'VMPP',
    'VVFIN',
    'VVIMP',
    'VVINF',
    'VVIZU',
    'VVPP',
]


class german_embedder:

    def __init__(self):
        self.nlp = spacy.load('de_core_news_sm')

    def embed(self, text):
        '''Embeds the given text and returns a np array/vector'''
        # At the end call np.array()
        doc = self.nlp(text)
        # This are all the lammata of the pos we define
        relevant_lemma = [(token.lemma_) for token in doc if token.tag_ in german_pos_tags]
        print(relevant_lemma)
        dim = len(relevant_lemma)
        print('Found lemma: ' + str(dim))

        for lemma in relevant_lemma:
            # foreach lemma, we create an embedding vector
            v = []


test_text = '''
Herr Wissing, Herr Theurer, das ist Augenwischerei. Strecken müssen in großem Umfang reaktiviert, mit Blick auf die nötige Klimaneutralität mit Hochdruck elektrifiziert, Industriegebiete wieder ans Bahnnetz angeschlossen werden. Der Antrag, über den wir heute reden, ist Konsequenz aus der Empfehlung der Beschleunigungskommission Schiene. Schiene müssten jährlich elektrifiziert werden;
'''


def test():
    em = german_embedder()
    test = em.embed(test_text)


if __name__ == "__main__":
    test()
