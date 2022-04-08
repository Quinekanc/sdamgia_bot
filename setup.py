import os
import requests
import platform
import zipfile


if os.name == "nt" and platform.architecture()[0] == '64bit':
    if not os.path.exists("vips-dev-w64-web-8.12.2-static.zip"):
        content = requests.get("https://github.com/libvips/build-win64-mxe/releases/download/v8.12.2/"
                               "vips-dev-w64-web-8.12.2-static.zip").content
        with open("vips-dev-w64-web-8.12.2-static.zip", mode="wb") as file:
            file.write(content)

    if not os.path.exists("vips"):
        os.makedirs("vips")

    with zipfile.ZipFile("vips-dev-w64-web-8.12.2-static.zip", 'r') as zip:
        zip.extractall("vips/")
    os.remove("vips-dev-w64-web-8.12.2-static.zip")

    vipshome = os.path.abspath(os.getcwd()) + 'vips/vips-dev-8.12/bin/'
    os.environ['vips'] = vipshome

    print("Installed")
else:
    print("UNSUPPORTED OS")