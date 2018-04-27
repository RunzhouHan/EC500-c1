import json
from urllib.request import urlopen
import pymongo

connection = pymongo.MongoClient("mongodb://localhost")
db=connection.book
record1 = db.book_collection1
# record1.drop()
page = urlopen("https://gist.githubusercontent.com/tdreyno/4278655/raw/7b0762c09b519f40397e4c3e100b097d861f5588/airports.json")
parsed = json.loads(page.read())
for i in range(len(parsed)):
	record1.insert(parsed[i])




