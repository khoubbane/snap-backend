from http.server import BaseHTTPRequestHandler
import json
import yt_dlp

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data.decode('utf-8'))
        url = body.get('url', '')

        # Headers bach n-autorisiw l-frontend i-connecta
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

        if not url:
            self.wfile.write(json.dumps({"error": "3afak dkhl lien Snapchat s7i7"}).encode('utf-8'))
            return

        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                res = {
                    "success": True,
                    "download_url": info.get('url'),
                    "title": info.get('title', 'Vidéo Snapchat')
                }
                self.wfile.write(json.dumps(res).encode('utf-8'))
        except Exception as e:
            self.wfile.write(json.dumps({"error": "Ma 9dernach njbdo l-vidéo. T2ked bli lien public."}).encode('utf-8'))

    def do_OPTIONS(self):
        # Bach n-gériw CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()