import sqlite3

class DatabaseOfDOOM:
	def __init__(self):
		self.con = sqlite3.connect("DatabaseOfDOOM.db")
		self.cur = self.con.cursor()

	def makeDB(self):
		command = "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, color TEXT)"
		self.cur.execute(command)
		self.con.commit()

	def addUser(self, name, password, color):
		command = "INSERT INTO users (name, password, color) VALUES (?, ?, ?)"
		arguments = [name, password, color]
		self.cur.execute(command, arguments)
		self.con.commit()

	def getUserByUsername(self, name):
		command = "SELECT * FROM users WHERE name = ?"
		self.cur.execute(command, [name])
		user = self.cur.fetchone()
		return user
