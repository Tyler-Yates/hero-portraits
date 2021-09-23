import base64
import json
import os
from pathlib import Path

import requests

GENERATION_API_URL = "https://api.waifulabs.com/generate"

IMAGES_BASE_PATH = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", "images"))
Path(IMAGES_BASE_PATH).mkdir(parents=True, exist_ok=True)


def main():
    request_data = {
        "step": 0,
        "currentGirl": [],
        "size": 512
    }
    response = requests.post(GENERATION_API_URL, json=request_data)
    response.raise_for_status()

    response_data = json.loads(response.text)

    character_portraits = response_data["newGirls"]

    index = 0
    for character_portrait in character_portraits:
        image_string = character_portrait["image"]
        image_data = base64.b64decode(image_string)

        file_path = os.path.join(IMAGES_BASE_PATH, f'portrait{index}.png')
        while os.path.exists(file_path):
            index += 1
            file_path = os.path.join(IMAGES_BASE_PATH, f'portrait{index}.png')

        with open(file_path, 'wb') as f:
            f.write(image_data)


if __name__ == '__main__':
    main()
