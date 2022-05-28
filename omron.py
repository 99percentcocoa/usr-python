import main
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def usrGen():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        # input = u"सूर्यास्त के बाद आकाश को देखना कितना अच्छा लगता है।"
        inputJSON = request.get_json()
        usr1 = main.getUSR(inputJSON['input'])
    else:
        return 'Content-Type not supported!'
    return usr1

if __name__ == '__main__':
    app.run(debug=True)