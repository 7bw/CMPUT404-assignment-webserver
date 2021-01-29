#  coding: utf-8 
import socketserver
import os
# Copyright 2021 Bowei Li
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

response = {200: "HTTP/1.1 200 OK\r\n",
            301: "HTTP/1.1 301 Moved Permanently\r\n",
            404: "HTTP/1.1 404 Not Found\r\n",
            405: "HTTP/1.1 405 Method Not Allowed\r\n"}

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.code = 0
        self.data = self.request.recv(1024).strip()
        parsedData = self.data.split(b'\n')
        parse = parsedData[0].split(b' ')
        print ("Got a request of: %s\n" % self.data)

        self.root = "./www"
        s = parse[1].decode(encoding='UTF-8')
        path = self.root + s
        print(path)
        if parse[0] != b'GET':
            self.code = 405
            self.respond(path)
        else:
            path = self.check_path(path)
            self.respond(path)
        #self.request.sendall(bytearray("OK",'utf-8'))

    def check_path(self, path):
        print("path =:")
        print(path)
        result = ""
        end = path[-1]
        newPath = os.path.normpath(path)
        print("newPath =:")
        print(newPath)
        if not newPath.startswith(self.root[2:]):
            self.code = 404
            return None
        newPath = "./" + newPath
        if not os.path.exists(newPath):
            self.code = 404
            return None

        if os.path.exists(newPath):
            if end == "/":
                print("you got the right!")
                newPath += "/index.html"
                try:
                    self.code = 200
                    self.content = open(newPath, "r").read()
                    self.contentType = "text/html"
                    return newPath
                except IOError:
                    self.code = 404
                    return None
            else:
                print("you are wrong!")
                if path.endswith(".html"):
                    try:
                        self.code = 200
                        self.content = open(newPath, "r").read()
                        self.contentType = "text/html"
                        return newPath
                    except IOError:
                        self.code = 404
                        return None
                elif path.endswith(".css"):
                    try:
                        self.code = 200
                        self.content = open(newPath, "r").read()
                        self.contentType = "text/css"
                        return newPath
                    except IOError:
                        self.code = 404
                        return None
                else:
                    try:
                        self.code = 301
                        newPath += "/index.html"
                        self.content = open(newPath, "r").read()

                        return newPath
                    except IOError:
                        self.code = 404
                        return None



    def respond(self,path):
        print("code == : "+ str(self.code) )
        if self.code == 200:
            message = response[200] + "Location: http://127.0.0.1:8080/%s\r\n" %(path[2:])
            message += "Content-Type: " + self.contentType + "; charset=UTF-8\r\n"
            message += "Connection: close\r\n\r\n"
            message += self.content + "\r\n"
            print(message)
            self.request.sendall(bytearray(message,'utf-8'))
        elif self.code == 301:
            print("301 location!!!!")
            print(path)
            message = response[301] + "Location: http://127.0.0.1:8080/%s\r\n" %(path[2:])
            message += "Content-Type: text/html; charset=UTF-8\r\n"
            message += "Connection: close\r\n\r\n"
            message += self.content + "\r\n"
            print(message)
            self.request.sendall(bytearray(message,'utf-8'))
        elif self.code == 404:
            message = response[404] + "Content-Type: text/plain; charset=UTF-8\r\n"
            message += "Connection: close\r\n\r\n"
            message += "404 Not Found\r\n"
            
            print(message)
            self.request.sendall(bytearray(message,'utf-8'))

        elif self.code == 405:
            message = response[405]
            message += "Connection: close\r\n"
            print(message)
            self.request.sendall(bytearray(message,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
