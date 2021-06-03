# easy-gTTS-API

An easy to use [gTTS](https://cloud.google.com/text-to-speech) middleman built using `aiohttp`.

## Hosting

Docker is the preferred way to host an instance of the API.

Environment Variables:

* `EASY_GTTS_API_PORT`: Configures the webserver port. Default is `8080`.
* `EASY_GTTS_API_HOST`: Configures the webserver host. Default is `0.0.0.0`.

## API

### GET `/v1beta1/synthesize`

Returns TTS Speech from https://texttospeech.googleapis.com/v1beta1/text:synthesize.

Parameters:

* `?text=`: Text to be converted into speech.
* `?lang=en-US`: Language of the text to be converted into speech.
* `?voice=en-US-Wavenet-D`: Voice that will speak the text.
* `?encoding=MP3`: Audio encoding taht

### GET `/v1beta1/voices`

Returns a list of voices that can be used for synthesis from https://texttospeech.googleapis.com/v1beta1/voices.

Parameters:

* `?languageCode=None`: The language code to be searched.
