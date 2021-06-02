import os

from util.app import CustomApp

app = CustomApp()

for file in os.listdir("subapps/"):
    if file.endswith(".py"):
        full_path = "subapps/" + file
        app.load_subapp(os.path.splitext(full_path)[0].replace("/", "."))

if __name__ == "__main__":
    from os import environ

    from aiohttp import web

    port = int(environ.setdefault("EASY_GTTS_API_PORT", "8080"))
    host = environ.setdefault("EASY_GTTS_API_HOST", "0.0.0.0")

    web.run_app(app, host=host, port=port)
