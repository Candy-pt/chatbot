from flask import Flask, render_template, request, jsonify
from bot import process_query

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    response = process_query(user_message)
    return jsonify({'response': response['response']})

if __name__ == '__main__':
    app.run(debug=True)
    