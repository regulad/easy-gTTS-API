# easy-gTTS-API

An easy to use [gTTS](https://cloud.google.com/text-to-speech) middleman built using `aiohttp`.

## Hosting

Docker is the preferred way to host an instance of the API.

Environment Variables:

* `EASY_GTTS_API_PORT`: Configures the webserver port. Default is `8080`.
* `EASY_GTTS_API_HOST`: Configures the webserver host. Default is `0.0.0.0`.

Authentication:

Store a Google Cloud `SERVICE_ACCOUNT.JSON` in `/config`.

Versions:

There are two subapps included: `v1` and `v1beta1`, each mapping to Google's `v1` and `v1beta1` respectively.

Full URL example: `netloc/v1/synthesize` or `netloc/v1beta1/synthesize`

## API

### GET `/synthesize`

Returns TTS Speech from https://texttospeech.googleapis.com/v1beta1/text:synthesize.

Parameters:

* `?text=`: Text to be converted into speech.
* `?lang=en-US`: Language of the text to be converted into speech.
* `?voice=en-US-Wavenet-D`: Voice that will speak the text.
* `?encoding=MP3`: The encoding of the returned bytes.

### GET `/voices`

Returns a list of voices that can be used for synthesis from https://texttospeech.googleapis.com/v1beta1/voices.

Parameters:

* `?languageCode=None`: The language code to be searched.
