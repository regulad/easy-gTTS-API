# easy-gTTS-API

An easy to use gTTS middleman using `aiohttp`.

## Hosting

Docker is the preferred way to host an instance of the API.

Environment Variables:
* `EASY_GTTS_API_PORT`: Configures the webserver port. Default is `8080`.
* `EASY_GTTS_API_HOST`: Configures the webserver host. Default is `0.0.0.0`.

## API

### GET `/tts`
Returns TTS from `gTTS`.

Parameters:
* `?text=`: Text to be converted into speech.
* `?lang=en`: Language of the text to be converted into speech.
