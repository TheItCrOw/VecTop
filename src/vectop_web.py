from flask import Flask, jsonify, render_template, request
from vectop import vectop

app = Flask(__name__, template_folder='./web/templates', static_folder='./web/static')
vec = ''


def get_connection_string():
    with open('./embedder/pg_connection_string.txt', 'r') as f:
        return f.read()


def get_openai_api_key():
    with open('./embedder/openai_api_key.txt', 'r') as f:
        return f.read()


# Define a route for the homepage
@app.route('/')
def index():
    return render_template('html/index.html')


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
            # Here we extract the topics
            res = vec.extract_topics(text, lang)
            result['result'] = {
                'topics': res[0],
                'sources': res[1]
            }
            print(result)
            result['status'] = 200
    except Exception as ex:
        print("Couldn't extract topics from text: " + text)
        print("Language was: " + lang)
        print(ex)
    return jsonify(result)


if __name__ == '__main__':
    print("Loading vectop module...")
    vec = vectop(get_openai_api_key(), get_connection_string())
    print("Finished loading. Starting server.")
    app.run(port=5678, debug=True)
