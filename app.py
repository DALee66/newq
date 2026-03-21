from flask import Flask, request, jsonify
from flask_cors import CORS
import dashscope
from dashscope import Generation

app = Flask(__name__)
CORS(app)  # Разрешаем браузеру делать запросы к этому серверу

# Вставьте сюда ваш API ключ от DashScope
dashscope.api_key = 'ВАШ_API_КЛЮЧ'

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'Сообщение пустое'}), 400

    try:
        # Формируем запрос к модели Qwen
        # Используем модель qwen-turbo или qwen-plus
        response = Generation.call(
            model='qwen-turbo',
            messages=[
                {'role': 'system', 'content': 'Ты полезный ассистент.'},
                {'role': 'user', 'content': user_message}
            ],
            result_format='message'
        )

        if response.status_code == 200:
            bot_reply = response.output.choices[0].message.content
            return jsonify({'reply': bot_reply})
        else:
            return jsonify({'error': f'Ошибка API: {response.code}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Сервер запущен на http://127.0.0.1:5000")
    app.run(debug=True)