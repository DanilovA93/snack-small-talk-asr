import http.server
import socketserver
from http import HTTPStatus
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import Audio, load_dataset


# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large")
forced_decoder_ids = processor.get_decoder_prompt_ids(language="english", task="translate")



class Handler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/plain')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        audio = self.rfile.read(content_len)


        input_features = processor(audio, sampling_rate=16_000, return_tensors="pt").input_features

        # generate token ids
        predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
        # decode token ids to text
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)



        self._set_headers()
        self.wfile.write(transcription.encode())

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()


httpd = socketserver.TCPServer(('', 8000), Handler)
httpd.serve_forever()
