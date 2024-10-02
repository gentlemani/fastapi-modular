import os
from firebase_admin import firestore
from typing import Dict
from constants import ACCEPTED_FIELDS
from models.recipe import Recipe
class UserService:
    def __init__(self) -> None:
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.db = firestore.client()        
        
    def get_all_users(self) -> Dict[str,Dict[str,int]]:
        collection_ref = self.db.collection('Users')
        docs = list(collection_ref.stream())
        users = dict()
        for doc in docs:
            user_data = doc.to_dict()
            #Retrive only the necessary data (categories of the frecuency table)
            filtered_data = {key: user_data[key] for key in ACCEPTED_FIELDS if key in user_data}
            #Creates the Dict[str,Dict[str,int]] form.
            users[doc.id] = {k: v for k, v in filtered_data.items()}
        return users
    