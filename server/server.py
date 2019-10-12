#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from database import DatabaseOfDOOM
from urllib.parse import parse_qs
import json

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path.startswith("/users"):
			path = self.path.split("/")
			if len(path) < 3:
				#be more specific
				self.send400()
				return
			user = path[2]
			self.send_response(200)
			self.end_headers()
			self.wfile.write(bytes(json.dumps(DatabaseOfDOOM().getUserByUsername(user)),"utf-8"))
		else:
			self.send404()

	def do_POST(self):
		if self.path.startswith("/users"):
			try:
				body = parse_qs(self.getBody())
				name = body["name"][0]
				password = body["password"][0]
				color = body["color"][0]
			except:
				self.send400()
				return
			if DatabaseOfDOOM().addUser(name, password, color):
				self.send_response(200)
				self.send_header("Content-Type","application/json")
				self.end_headers()
				self.wfile.write(bytes(json.dumps(DatabaseOfDOOM().getUserByUsername(user)),"utf-8"))
			else:
				self.send400("User already exists")
		else:
			self.send404()

	def send400(self,message="Bad request: What are you trying to do?! (´・ω・｀)"):
		self.send_response(400)
		
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
	listen = ("", 8080)
	server = HTTPServer(listen, RequestHandler)

	db = DatabaseOfDOOM()
	db.makeDB()
	del db

	print("Listening...")
	server.serve_forever()

main()
