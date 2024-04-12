# Auto Podcast

This repository contains a very simple command-line interface application, that uses OpenAI GPT API to generate the full transcript for a podcast, and uses its text-to-speech API to generate voice for the transcript parts. Then, it uses `pydub` to concatenate all parts into a single podcast `mp3` file.

## Running

First, you should install the dependencies:

* `ffmpeg` or `avconv` for `pydub` to work:

```
$ apt-get update && apt-get -y install ffmpeg
```

Then, you should install the Python dependencies:

```
$ pip install -r requirements.txt
```

After that, you should set the OpenAI API key as an environment variable:

```
$ export OPENAI_API_KEY=sk-something
```

Finally, you can run the script:

```
$ python main.py --topic "A podcast about love, how people love each other, and the symbols for love" --output "love-podcast"
```

Fully running this script produces the `love-podcast.md` and `love-podcast.mp3` files.

Have fun!

## License

Copyright 2024 Botond János Kovács <botondjanoskovacs@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
