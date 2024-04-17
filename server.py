import http.server
import socketserver
from http import HTTPStatus
import openai
from pydub import AudioSegment


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



        buffer = io.BytesIO()
        buffer.name = "fname"
        audio.export(buffer, format="mp3")
        transcript = openai.Audio.transcribe("whisper-1", buffer)


        self._set_headers()
        self.wfile.write(transcript.encode())

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.end_headers()


httpd = socketserver.TCPServer(('', 8000), Handler)
httpd.serve_forever()
