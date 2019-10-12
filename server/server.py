#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from database import DatabaseOfDOOM
from urllib.parse import parse_qs
import json

import BaseHTTPServer, SimpleHTTPServer
import ssl


class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.startswith("/users"):
			path = self.path.split("/")
			if len(path) < 3:
				self.send400()
				return
			user = path[2]
			self.send_response(200)
			self.send_header("Content-Type","application/json")
			self.send_header("Access-Control-Allow-Origin","*")
			self.end_headers()
			self.wfile.write(bytes(json.dumps(DatabaseOfDOOM().getUserByUsername(user)),"utf-8"))
		else:
			self.send404()

	def do_POST(self):
		if self.path.startswith("/users"):
			try:
				body = self.getBody()
				print(body)
				parsedBody = json.loads(body)
				print(parsedBody)
				name = parsedBody["name"]
				password = parsedBody["password"]
				color = parsedBody["color"]
				"""
				body = parse_qs(self.getBody())
				name = body["name"][0]
				password = body["password"][0]
				color = body["color"][0]
				"""
			except:
				self.send400()
				return
			if DatabaseOfDOOM().addUser(name, password, color):
				self.send_response(200)
				self.send_header("Content-Type","application/json")
				self.send_header("Access-Control-Allow-Origin","*")
				self.end_headers()
				self.wfile.write(bytes(json.dumps(DatabaseOfDOOM().getUserByUsername(name)),"utf-8"))
			else:
				self.send400("User already exists")
		else:
			self.send404()

	def do_OPTIONS(self):
		self.send_response(200, "ok")
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
		self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
		self.send_header("Access-Control-Allow-Headers", "Content-Type")
		self.end_headers()

	def send400(self,message="Bad request: What are you trying to do?! (´・ω・｀)"):
		self.send_response(400)
		self.send_header("Access-Control-Allow-Origin","*")
		
		self.end_headers()
		self.wfile.write(bytes(message, "utf-8"))

	def send403(self):
		self.send_response(403)
		self.end_headers()
		self.wfile.write(bytes("Not Authenticated", "utf-8"))
	
	def send404(self):
		self.send_response(404)
		self.end_headers()
		self.wfile.write(bytes("Not found", "utf-8"))

	def getBody(self):
		length = self.headers["Content-Length"]
		return self.rfile.read(int(length)).decode("utf-8")

def main():
	#listen = ("", 80)
	#server = HTTPServer(listen, RequestHandler)

	db = DatabaseOfDOOM()
	db.makeDB()
	del db

	print("Listening...")
	server.serve_forever()
	httpd = BaseHTTPServer.HTTPServer(('localhost', 4443), HTTPServer.RequestHandler)
	httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
	httpd.serve_forever()

main()
