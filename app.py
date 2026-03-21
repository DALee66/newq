from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Инициализация клиента DeepSeek
# Мы берем ключ из переменной окружения
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'), 
    base_url="https://api.deepseek.com"
)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'Сообщение пустое'}), 400

    try:
        # Запрос к модели DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",  # Или "deepseek-coder"
            messages=[
                {"role": "system", "content": "Ты полезный ассистент."},
                {"role": "user", "content": user_message}
            ],
            stream=False
        )

        bot_reply = response.choices[0].message.content
        return jsonify({'reply': bot_reply})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)