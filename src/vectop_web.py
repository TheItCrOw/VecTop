from flask import Flask, jsonify, render_template, request
from vectop import Vectop
from legal_vectop import LegalVectop


def get_connection_string():
    with open('./embedder/pg_connection_string.txt', 'r') as f:
        return f.read()


def get_openai_api_key():
    with open('./embedder/openai_api_key.txt', 'r') as f:
        return f.read()


app = Flask(__name__, template_folder='./web/templates', static_folder='./web/static')
vec = Vectop(get_openai_api_key(), get_connection_string())
legal_vec = LegalVectop(get_openai_api_key(), get_connection_string())


# Define a route for the homepage
@app.route('/')
def index():
    return render_template('html/index.html')


@app.route('/api/legal/extract', methods=['POST'])
def extract_reference():
    result = {
        'status': 400,
    }

    try:
        if request.is_json:
            data = request.get_json()
            text = str(data.get('text'))
            take = str(data.get('confidence'))
            # Here we extract the topics
            res = legal_vec.extract_references(text, take)
            result['result'] = {
                'references': res
            }
            result['status'] = 200
            print(result)
    except Exception as ex:
        print("Couldn't extract references from text: ")
        result['error'] = ex
        print(ex)
    return jsonify(result)


@app.route('/api/extract', methods=['POST'])
def extract_topic():
    result = {
        'status': 400,
    }

    try:
        if request.is_json:
            data = request.get_json()
            lang = str(data.get('lang'))
            text = str(data.get('text'))
            take = str(data.get('confidence'))
            corpus = str(data.get('corpus'))
            # Here we extract the topics
            res = vec.extract_topics(text, lang, take, corpus)
            result['result'] = {
                'topics': res[0],
                'sources': res[1]
            }
            result['status'] = 200
    except Exception as ex:
        print("Couldn't extract topics from text: ")
        print("Language was: ")
        result['error'] = ex
        print(ex)
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5678, debug=True)
