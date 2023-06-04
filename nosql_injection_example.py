#################### Setup MondoDB: ####################

from pymongo import MongoClient

def get_database():
   # Provide the mongodb url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://127.0.0.1:27017/" # 27017 is the default MongoDB port
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
   # Create the database
   return client['user_database']

db = get_database()

def initialize_mongodb():
    users_collection = db["users"] # collection named "users" in the database
    users_collection.drop() # Clear the collection
    # Insert documents into the "users" database:
    user_1 = {
        "_id" : "U1IT00001",
        "uname" : "Alice",
        "pw" : "qwerty123",
        "credit_card" : "4775462337863648",
    }
    user_2 = {
        "_id" : "U1IT00002",
        "uname" : "Bob",
        "pw" : "correct-horse-battery-staple",
        "credit_card" : "4775468105507721",
    }
    users_collection.insert_many([user_1, user_2])
    # You can check the contents in the mongosh using:
    #   use user_database
    #   db.users.find()

initialize_mongodb()



#################### Setup HTTP server: ####################

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

from urllib.parse import urlparse, parse_qs

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>NoSQL Injection Example</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<h1>Login</h1>", "utf-8"))
            self.wfile.write(bytes("<form action=\"/profile.html\">", "utf-8"))
            self.wfile.write(bytes("<label for=\"uname\">Username:</label><input type=\"text\" id=\"uname\" name=\"uname\"><br><br>", "utf-8"))
            self.wfile.write(bytes("<label for=\"pw\">Password:</label><input type=\"password\" id=\"pw\" name=\"pw\"><br><br>", "utf-8"))
            self.wfile.write(bytes("<input type=\"submit\" value=\"Login\">", "utf-8"))
            self.wfile.write(bytes("</form>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        elif self.path.startswith("/profile.html"):
            # Parse URL (e.g. "http://localhost:8080/profile.html?uname=foo&pw=bar"):
            parsed_url = urlparse(self.path)
            try:
                uname = parse_qs(parsed_url.query)['uname'][0]
                pw = parse_qs(parsed_url.query)['pw'][0]
                print(f"Login attempt as user '{uname}' with password '{pw}'")

                """
                # Safe against injection attack:
                matches = db.users.find({
                    "uname": uname,
                    "pw": pw
                })
                """

                # Succeptible to injection attack: http://localhost:8080/profile.html?uname=Alice&pw=' || '1'=='1
                matches = db.users.find({"$where": f"this.uname == '{uname}' && this.pw == '{pw}'"})
                
                matches_list = list(matches)
                if len(matches_list) == 0:
                    self.send_response(401)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("<html><head><title>Wrong Credentials</title></head>", "utf-8"))
                    self.wfile.write(bytes("<body>", "utf-8"))
                    self.wfile.write(bytes("<h1>Wrong Credentials</h1>", "utf-8"))
                    self.wfile.write(bytes("</body></html>", "utf-8"))
                else:
                    match = matches_list[0]
                    uname = match["uname"]
                    credit_card = match["credit_card"]
                    # Show sensitive information:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(bytes("<html><head><title>Profile</title></head>", "utf-8"))
                    self.wfile.write(bytes("<body>", "utf-8"))
                    self.wfile.write(bytes("<h1>Profile</h1>", "utf-8"))
                    self.wfile.write(bytes("Username: %s<br><br>" % uname, "utf-8"))
                    self.wfile.write(bytes("Credit Card: %s" % credit_card, "utf-8"))
                    self.wfile.write(bytes("</body></html>", "utf-8"))
            except KeyError as e:
                print(f"KeyError: {e}")
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>400 Bad Request</title></head>", "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                self.wfile.write(bytes("<h1>400 Bad Request</h1>", "utf-8"))
                self.wfile.write(bytes("</body></html>", "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>404 Not found</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<h1>404 Not found</h1>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
       
webServer = HTTPServer((hostName, serverPort), MyServer)
print("Server started http://%s:%s" % (hostName, serverPort))

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
print("Server stopped.")
