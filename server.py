from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import time
import config

app = Flask(__name__)
CORS(app)

# Настройки из вашего файла
api_key = config.token
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}


@app.route('/')
def index():
    return render_template("main.html")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    
    # Логика из вашего скрипта
    payload = {
        "height": 1024,
        "width": 1024,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
        "prompt": prompt
    }
    
    try:
        # 1. Создаем задание
        res = requests.post("https://cloud.leonardo.ai", json=payload, headers=headers)
        gen_id = res.json()['sdGenerationJob']['generationId']
        
        # 2. Ждем (у вас было 20 сек)
        time.sleep(20)
        
        # 3. Забираем результат
        res_url = f"https://cloud.leonardo.ai/{gen_id}"
        data = requests.get(res_url, headers=headers).json()
        image_url = data["generations_by_pk"]["generated_images"][0]["url"]
        
        return jsonify({"image_url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)