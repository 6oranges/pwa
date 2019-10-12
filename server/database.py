import sqlite3
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
class DatabaseOfDOOM:
	def __init__(self):
		self.con = sqlite3.connect("DatabaseOfDOOM.db")
		self.con.row_factory = dict_factory
		self.cur = self.con.cursor()

	def makeDB(self):
		command = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT UNIQUE, password TEXT, color TEXT)"
		self.cur.execute(command)
		self.con.commit()

	def addUser(self, name, password, color):
		if self.getUserByUsername(name) == None:
			command = "INSERT INTO users (name, password, color) VALUES (?, ?, ?)"
			arguments = [name, password, color]
			self.cur.execute(command, arguments)
			self.con.commit()
			return True
		else:
			return False

	def getUserByUsername(self, name):
		command = "SELECT * FROM users WHERE name = ?"
		self.cur.execute(command, [name])
		user = self.cur.fetchone()
		return user
	def __del__(self):
		self.con.close()