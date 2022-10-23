from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def path_exist(self):
        print("InHERE" + self.path)
        if not(os.path.exists(self.path)):
            self.send_error(404, message=None, explain=None)
        else:
            return 1

    def has_been_modified(self):
        if not(": " + str(os.path.getmtime(self.path))) == str(self.headers["If-Modified-Since"]):
            return 1

    def do_GET(self):
        self.path = os.getcwd() + "/" + self.path
        print(self.path)
        if self.path_exist() and self.has_been_modified():
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Last-Modified:", os.path.getmtime(self.path))
            self.end_headers()
            self.wfile.write(bytes("<html><head>The server does not accept persistent connections.</head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        elif self.path_exist() and not(self.has_been_modified()):
            self.send_error(304, message=None, explain=None)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")