import http.server
import socketserver
import json
import nemo.collections.asr as nemo_asr
from http import HTTPStatus


asr_model = nemo_asr.models.ASRModel.from_pretrained("stt_en_fastconformer_transducer_large")


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
        file = self.rfile.read(content_len)
        path_to_file = "./files/demofile.wav"
        f = open(path_to_file, "wb")
        f.write(file)
        f.close()
        transcript = asr_model.transcribe([path_to_file])
        text = transcript[0][0]
        self._set_headers()
        self.wfile.write(text.encode())

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()


httpd = socketserver.TCPServer(('', 8001), Handler)
httpd.serve_forever()