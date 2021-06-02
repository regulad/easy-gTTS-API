from os import environ
from io import BytesIO

from aiohttp import web
from gtts import gTTS, gTTSError, lang


port = int(environ.setdefault("EASY_GTTS_API_PORT", "8080"))
host = environ.setdefault("EASY_GTTS_API_HOST", "0.0.0.0")


languages = lang.tts_langs()
routes = web.RouteTableDef()


@routes.get("/tts")
async def tts_route(request: web.Request):
    text = request.query.get("text")
    language = request.query.get("language", "en")

    if language not in languages:
        raise web.HTTPBadRequest(reason=f"{language} is not a valid language.")

    buffer = BytesIO()

    try:
        gTTS(text=text, lang=language).write_to_fp(buffer)
    except (AssertionError, ValueError, RuntimeError) as e:
        raise web.HTTPBadRequest(reason=str(e))
    except gTTSError as e:  # Likely means that something went wrong on our side or Google's side.
        if e.rsp is not None:
            raise web.HTTPInternalServerError(reason=e.rsp.content.decode())
        raise

    stream_response = web.StreamResponse()
    stream_response.content_type = "audio/mp3"
    await stream_response.prepare(request)
    await stream_response.write(buffer.getvalue())
    await stream_response.write_eof()

    return stream_response


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host=host, port=port)
