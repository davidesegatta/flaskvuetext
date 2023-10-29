from flask import Flask, jsonify, request
from flask_cors import CORS
from stanza import Pipeline


# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

nlp = Pipeline('en')
#content = "These are simple sentences. And that's another one"
content = "These are horrific sentences. You are wonderful"

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/lemmatizza', methods=['POST'])
def lemmatizza():
    inpost = request.get_json
    print(type(inpost))
    text = inpost.get('text')
    out = []
    doc = nlp(text) # oggetto di tipo doc processato da Stanza
    for sent in doc.sentences:
        for word in sent.words:
            out.append(word.lemma)
    return out

@app.route('/sentiment_post', methods=['POST'])
def sentiment_analysis_post():
    inpost = request.get_json()
    text = inpost.get('text')
    sentiment = {0:'negativo',
                 1:'neutro',
                 2:'positivo'}
    out = []
    doc = nlp(text) # oggetto di tipo doc processato da Stanza
    for sent in doc.sentences:
        convertito = sentiment.get(sent.sentiment)
        out.append(f"La frase: {sent.text} ha il sentimento: {convertito}")
    return out

@app.route('/sentiment_simple', methods=['GET'])
def sentiment_analysis():
    sentiment = {0:'negativo',
                 1:'neutro',
                 2:'positivo'}
    out = []
    doc = nlp(content) # oggetto di tipo doc processato da Stanza
    for sent in doc.sentences:
        convertito = sentiment.get(sent.sentiment)
        out.append(f"La frase: {sent.text} ha il sentimento: {convertito}")
    return out

if __name__ == '__main__':
    app.run()
