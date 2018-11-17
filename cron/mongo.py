import pymongo
import vars

client = pymongo.MongoClient(connectTimeoutMS=3 * 1000,
                             socketTimeoutMS=3*1000,
                             wtimeout=3,
                             serverSelectionTimeoutMS=3*1000)
db = client.get_database(vars.mongo['db'])
bookmaker = db.get_collection('bookmaker')  # type: pymongo.collection.Collection
