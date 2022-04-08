import os
import requests
import pyvips
import uuid
from PIL import Image

imageFolder = "image_cache"

def InitImageUtils():
    if not os.path.exists(imageFolder):
        os.makedirs(imageFolder)


def GetPng(imageUrl: str):
    content = requests.get(imageUrl, allow_redirects=True).content
    fileName = str(uuid.uuid4()) + ".svg"

    with open(f"{imageFolder}/{fileName}", mode="wb") as file:
        file.write(content)

    img = pyvips.Image.new_from_file(f"{imageFolder}/{fileName}", access="sequential", dpi=300)
    img.write_to_file(f"{imageFolder}/{fileName.replace('.svg', '.png')}")

    os.remove(f"{imageFolder}/{fileName}")

    image = Image.open(f"{imageFolder}/{fileName.replace('.svg', '.png')}")
    background = Image.new('RGBA', image.size, color="white")
    Image.alpha_composite(background, image)\
        .save(f"{imageFolder}/{fileName.replace('.svg', '.png')}")

    with open(f"{imageFolder}/{fileName.replace('.svg', '.png')}", mode="rb") as file:
        uploadFile = {"file": file}
        r = requests.post("http://misha133.ru:30303/", files=uploadFile)
    os.remove(f"{imageFolder}/{fileName.replace('.svg', '.png')}")

    return r.url

