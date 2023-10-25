from vectop import vectop
import os

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


if __name__ == "__main__":
    v = vectop(get_openai_api_key(), get_connection_string())
    print("Loaded VecTop module")
    topics = v.extract_topics(example, 'de-DE')
    print(topics)
