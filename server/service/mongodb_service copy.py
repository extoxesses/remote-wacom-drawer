import os
from pymongo import MongoClient

from server import logging
from server.models import EnrollRole


class MongoDbService :
    logger = logging.getLogger(__name__)
    _instance = None
    
    def __init__(self) :
        if MongoDbService._instance is not None:
            raise Exception("This class is a singleton!")
        self.logger.debug('MongoDbService initialized')
        
        print(os.getenv('MONGO_URI'))
        print(os.getenv('MONGO_DB'))

        MongoDbService._instance = self
        try:
            self._client = MongoClient(os.getenv('MONGO_URI'))
            self._database = self._client[os.getenv('MONGO_DB')]
            self.logger.info('MongoDB connection enstablised')
        except Exception as e:
            self.logger.error('Error connecting to MongoDB:', e)
            raise e

    @classmethod
    def instance(cls):
        if cls._instance is None :
            cls._instance = MongoDbService()
        return cls._instance

    def upsert_client(self, session_id : str, role : EnrollRole):
        return self._database['sessions'].update_one(
            { '_id': session_id },
            { '$set': { 'role': role } },
            upsert=True
        )

    def create_room(self, room_id : str):
        return self._database['rooms'].update_one(
            { '_id': room_id },
            { '$set': { 'viewers': [] } },
            upsert=True
        )
    
    def add_viewer_to_room(self, room_id : str, viewer_id : str):
        return self._database['rooms'].update_one(
            { '_id': room_id },
            { '$push': { 'viewers': viewer_id } },
            upsert=True
        )

    def remove_viewer_from_room(self, room_id : str, viewer_id : str):
        return self._database['rooms'].update_one(
            { '_id': room_id },
            { '$pull': { 'viewers': viewer_id } },
            upsert=True
        )

# # Create or get collection
# collection = db['drawings']

# # Example CRUD operations
# def insert_drawing(drawing_data):
#     result = collection.insert_one(drawing_data)
#     return result.inserted_id

# def get_drawing(drawing_id):
#     return collection.find_one({'_id': drawing_id})

# def get_all_drawings():
#     return list(collection.find())

# def update_drawing(drawing_id, new_data):
#     return collection.update_one(
#         {'_id': drawing_id},
#         {'$set': new_data}
#     )

# def delete_drawing(drawing_id):
#     return collection.delete_one({'_id': drawing_id})

# # Example usage
# if __name__ == "__main__":
#     # Example data
#     sample_drawing = {
#         'name': 'Test Drawing',
#         'points': [[0, 0], [1, 1], [2, 2]],
#         'timestamp': '2024-03-14'
#     }
    
#     # Insert
#     doc_id = insert_drawing(sample_drawing)
#     print(f"Inserted document ID: {doc_id}")
    
#     # Retrieve
#     drawing = get_drawing(doc_id)
#     print(f"Retrieved drawing: {drawing}")