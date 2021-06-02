import json

from aiohttp import web, ClientSession

from asyncgTTS import AsyncGTTSSession

subapp = web.Application()
routes = web.RouteTableDef()

with open("config/SERVICE_ACCOUNT.JSON") as service_account_json:
    service_account_dict = json.load(service_account_json)

subapp["clientsession"] = ClientSession()
subapp["ttsclientsession"] = AsyncGTTSSession.from_service_account(
    service_account_dict, client_session=subapp["clientsession"], endpoint="https://texttospeech.googleapis.com/v1/",
)


@routes.get("/synthesize")
async def tts_route(request: web.Request):
    text = request.query.get("text")

    if text is None:
        raise web.HTTPBadRequest(reason="No input text was provided.")

    async with subapp["ttsclientsession"] as tts_client_session:
        audio_bytes = await tts_client_session.synthesize(text)

    stream_response = web.StreamResponse()
    stream_response.content_type = "audio/mp3"
    await stream_response.prepare(request)
    await stream_response.write(audio_bytes)
    await stream_response.write_eof()

    return stream_response


subapp.add_routes(routes)


def setup(app: web.Application):
    app.add_subapp("/v1/", subapp)
