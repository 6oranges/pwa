#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(bytes("OK", "utf-8"))

def main():
	listen = ("127.0.0.1", 8080)
	server = HTTPServer(listen, RequestHandler)
	print("Listening...")
	server.serve_forever()

main()
