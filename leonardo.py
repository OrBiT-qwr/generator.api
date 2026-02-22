import json
import requests
import time
import config


api_key = config.token
authorization = "Bearer %s" % api_key


headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

url = "https://cloud.leonardo.ai/api/rest/v1/generations"


def generate_image(prompt, filename="result.jpg"):
    payload = {
        "height": 1024,
        "width": 1024,
        "modelId": "7b592283-e8a7-4c5a-9ba6-d18c31f258b9",
        "prompt": prompt
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code)
    generation_id = response.json()['sdGenerationJob']['generationId']
    time.sleep(20)
    result_url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id
    response = requests.get(result_url, headers=headers)
    data = response.json()
    image_url = data["generations_by_pk"]["generated_images"][0]["url"]
    image_data = requests.get(image_url).content
    with open(filename, "wb") as file:
        file.write(image_data)
    return image_url