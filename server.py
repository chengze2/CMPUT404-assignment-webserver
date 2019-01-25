#  coding: utf-8
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.message = ""
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        self.data = self.data.split(b'\r\n')[0].split(b' ')
        try:
            action = self.data[0].decode("utf-8")
        except:
            pass
        try:
            dirc = self.data[1].decode("utf-8")
            if (dirc[0] != "/"):
                dirc = "/" + dric
        except:
            dirc = "/"
        try:
            http_version = self.data[2].decode("utf-8")
        except:
            http_version = "HTTP/1.1"
        self.message += http_version + " "
        self.path = "www"
        if(dirc[0]!="/"):
            self.path += "/"
        self.path += dirc
        if(action != "GET"):
            self.message += "405 Method Not Allowed \r\n"
        elif(os.path.exists(self.path) and (os.getcwd() in os.path.abspath(self.path))
            and (action=="GET")):
            redirect = False
            if(os.path.isdir(self.path)):
                if(self.path[-1]!="/"):
                    self.path += "/"
                    redirect = True
                self.path += "index.html"
                if(os.path.exists(self.path)):
                    if(redirect):
                        self.message += "301 Moved Permanently \r\n\r\n"
                        self.message += "Location: http://127.0.0.1:8080/" + self.path + "/index.html"
                    else:
                        self.message += "200 OK \r\n"
                        self.addType(self.path)
                        file = open(self.path)
                        self.message += file.read()
                else:
                    self.message += "404 Not FOUND \r\n"
            elif(os.path.isfile(self.path)):
                self.message += "200 OK \r\n"
                self.addType(self.path)
                file = open(self.path)
                self.message += file.read()
        else:
            self.message += "404 Not FOUND \r\n"

        # reference:
        # https://uofa-cmput404.github.io/cmput404-slides/04-HTTP.html
        # https://code.tutsplus.com/tutorials/http-headers-for-dummies--net-8039
        self.response()

    def response(self):
        #print(self.message)
        self.request.sendall(bytearray(self.message,'utf-8'))

    def addType(self, path):
        if(".css" in path):
            self.message += "Content-Type: text/css; \r\n\r\n"
        elif(".html" in path):
            self.message += "Content-Type: text/html; \r\n\r\n"
        else:
            self.message += "Content-Type: text/plain; \r\n\r\n"


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
