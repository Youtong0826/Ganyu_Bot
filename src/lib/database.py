from pymongo import MongoClient

client = MongoClient("mongodb+srv://Ganyu-bot-cloud-db:4Yhg2yMn20UpRQvn@ganyu-bot.7pvjkku.mongodb.net/?retryWrites=true&w=majority")

class MongoDB:
    def __init__(self,db:str,id:str) -> None:
        self.col = client[str(db)][str(id)]

    def set(self,data:dict):
        self.col.insert_one(data)

    def set_many(self,data:list):
        self.col.insert_many(data)

    def update(self,query,new:dict):
        self.col.update_one(query,{"$set":new})

    def update_all(self,query,new):
        self.col.update_many(query,{"$set":new})

    def read_first(self,id:int=0):
        return self.col.find_one({},{"_id":id})

    def read_all(self,query:dict={},is_read:dict={},id:bool=False):
        is_read["_id"] = 0 if id == False else 1

        datas = [data for data in self.col.find(query,is_read)]
        return datas

    def delete(self,data):
        self.col.delete_one(data)

    def delete_all(self,query:dict={}):
        self.col.delete_many(query)

    def drop(self):
        self.col.drop()

    @property
    def data(self):
        return self.read_all()

