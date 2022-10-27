from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

hostName = "localhost"
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def path_exist(self): # Determine if the path requested exists. If not, send a 404. If it has moved, send a 301.
        if not(os.path.exists(os.getcwd() + self.path)):
            if self.has_moved():
                #HTTP servers. Python 3.10.8 documentation. (n.d.). Retrieved October 26, 2022, from https://docs.python.org/3/library/http.server.html
                # I used this source for specific python functions and utilities such as send_error().
                self.send_error(301, message="New location:" + str(self.where_moved()), explain=None)
            else:
                self.send_error(404, message=None, explain=None)
        else:
            return 1

    def has_moved(self): # If the file has moved from where it is currently being requested
        f = open("moved", "r")
        data = f.read()
        for i in data.split("\n"):
            if self.path in i:
                x = i.split()
                if self.path == x[0]:
                    return 1
                else:
                    return 0
                break

    def where_moved(self): # Return where the requested file has moved to
        f = open("moved", "r")
        data = f.read()
        for i in data.split("\n"):
            if self.path in i:
                x = i.split()
                return x[1]
        print("Cannot find where moved")
        
    def has_been_modified(self): # Determine if the file modification time is different from the "If-Modified-Since" header value.
        if not(": TODO: DELETEME" + str(os.path.getmtime(os.getcwd() + self.path))) == str(self.headers["If-Modified-Since"]):
            return 1


    def do_HEAD(self): # Webapp starts here with a HEAD request
# OS - miscellaneous operating system interfaces. Python 3.10.8 documentation. (n.d.). Retrieved October 26, 2022, from https://docs.python.org/3/library/os.html 
# I used this source to find specific os functions and commands such as os.getcwd().
        if self.path_exist() and self.has_been_modified(): # If the path exists and has been modified.
            self.send_response(200)
            if self.path == "/index.html":
                self.path = os.getcwd() + self.path
                self.send_header("Content-type", "text/html")
                self.send_header("Last-Modified:", os.path.getmtime(self.path))
                self.end_headers()
            elif self.path == "/images/fluffyDog1.jpg":
                self.path = os.getcwd() + self.path
                self.send_header("Content-type", "image/jpg")
                self.send_header("Last-Modified:", os.path.getmtime(self.path))
                self.end_headers()
            elif self.path == "/images/yapperDog1.jpg":
                self.path = os.getcwd() + self.path
                self.send_header("Content-type", "image/jpg")
                self.send_header("Last-Modified:", os.path.getmtime(self.path))
                self.end_headers()
                #https://www.pexels.com/video/a-dog-playing-in-the-snow-7481862/
            elif self.path == "/images/dogRunning.mp4":
                self.path = os.getcwd() + self.path
                self.send_header("Content-type", "video/mp4")
                self.send_header("Last-Modified:", os.path.getmtime(self.path))
                self.end_headers()
        elif self.path_exist() and not(self.has_been_modified()): # If the path exists, but it hasn't been modified, send a 304
            self.send_error(304, message=None, explain=None)



    def do_GET(self): # Webapp starts here with a GET request
        if self.path_exist() and self.has_been_modified(): # If the path exists and has been modified.
            f = open(os.getcwd() + self.path, "rb")
            data = f.read()
            self.send_response(200)
            if self.path == "/index.html":
                self.path = os.getcwd() + self.path
                self.send_header("Content-type", "text/html")
                self.send_header("Last-Modified:", os.path.getmtime(self.path))
                self.end_headers()
                self.wfile.write(data)
                # Barber, R. G., Cirino, M., Ramirez, R., &amp; O'Neill, S. (2022, May 26). Dog breeds are a behavioral myth... sorry! NPR. Retrieved October 26, 2022, from https://www.npr.org/2022/05/25/1101178609/dog-breeds-are-a-behavioral-myth-sorry 
            elif self.path == "/images/fluffyDog1.jpg":
                self.path = os.getcwd() + self.path
                self.send_header("Content-type", "image/jpg")
                self.send_header("Last-Modified:", os.path.getmtime(self.path))
                self.end_headers()
                self.wfile.write(data)
                #Dogs. Linda W. Yezak. (n.d.). Retrieved October 26, 2022, from https://lindayezak.com/tag/dogs/ 
            elif self.path == "/images/yapperDog1.jpg":
                self.path = os.getcwd() + self.path
                self.send_header("Content-type", "image/jpg")
                self.send_header("Last-Modified:", os.path.getmtime(self.path))
                self.end_headers()
                self.wfile.write(data)
                # A dog playing in the snow free stock video footage. Pexels. (n.d.). Retrieved October 27, 2022, from https://www.pexels.com/video/a-dog-playing-in-the-snow-7481862/ 
            elif self.path == "/images/dogRunning.mp4":
                self.path = os.getcwd() + self.path
                self.send_header("Content-type", "video/mp4")
                self.send_header("Last-Modified:", os.path.getmtime(self.path))
                self.end_headers()
                self.wfile.write(data)

        elif self.path_exist() and not(self.has_been_modified()): # If the path exists, but it hasn't been modified, send a 304
            self.send_error(304, message=None, explain=None)




# Create a python web server. Create a Python Web Server - Python Tutorial. (2021). Retrieved October 26, 2022, from https://pythonbasics.org/webserver/ 
# I used this source for the code below. The code below comes straight from this source. This code essentially sets up the webserver.
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try: # Keep running the server until a KeyboardIterrupt
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")