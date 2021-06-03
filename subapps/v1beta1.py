import json

from aiohttp import web, ClientSession

from asyncgTTS import (
    AsyncGTTSSession, ServiceAccount, TextSynthesizeRequestBody, SynthesisInput, VoiceSelectionParams, AudioConfig,
    AudioEncoding
)


subapp = web.Application()
routes = web.RouteTableDef()

with open("config/SERVICE_ACCOUNT.JSON") as service_account_json:
    service_account_dict = json.load(service_account_json)

subapp["clientsession"] = ClientSession()
subapp["serviceaccount"] = ServiceAccount.from_service_account_dict(service_account_dict)
subapp["ttsclientsession"] = AsyncGTTSSession.from_service_account(
    subapp["serviceaccount"], client_session=subapp["clientsession"],
    endpoint="https://texttospeech.googleapis.com/v1beta1/",
)


@routes.get("/synthesize")
async def tts_route(request: web.Request):
    text = request.query.get("text")
    lang = request.query.get("lang", "en-US")
    voice = request.query.get("voice", "en-US-Wavenet-D")
    encoding = request.query.get("encoding", "MP3")

    if text is None:
        raise web.HTTPBadRequest(reason="No input text was provided.")

    synthesis_input = SynthesisInput(text)
    synthesis_voice = VoiceSelectionParams(lang, voice)

    try:
        synthesis_encoding = AudioConfig(AudioEncoding(encoding.upper()))
    except ValueError:
        raise web.HTTPBadRequest(reason=f"{encoding} is not a valid encoding.")

    text_synthesize_request_body = TextSynthesizeRequestBody(
        synthesis_input, voice_input=synthesis_voice, audio_config_input=synthesis_encoding
    )

    audio_bytes = await subapp["ttsclientsession"].synthesize(text_synthesize_request_body)

    stream_response = web.StreamResponse()
    stream_response.content_type = f"audio/{encoding.lower()}"
    await stream_response.prepare(request)
    await stream_response.write(audio_bytes)
    await stream_response.write_eof()

    return stream_response


@routes.get("/voices")
async def tts_voices(request: web.Request):
    language_code = request.query.get("languageCode")

    response_json = await subapp["ttsclientsession"].get_voices(language_code=language_code)

    return web.json_response(response_json)


subapp.add_routes(routes)


def setup(app: web.Application):
    app.add_subapp("/v1beta1/", subapp)
