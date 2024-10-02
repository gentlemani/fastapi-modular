import pandas as pd
import pickle
import os
import uuid
from typing import List, Dict
from firebase_admin import firestore,storage
from models.recipe import Recipe
from fastapi import UploadFile

class RecipeService:
    def __init__(self) -> None:
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.db = firestore.client()
        self.categories = None
        
    def get_categories(self)->list|None:
        return self.categories
    
    def store_recipe(self,recipe:Recipe) -> str:
        recipe_dict = recipe.model_dump()
        created_time, doc_ref = self.db.collection("Recetas").add(recipe_dict)
        return doc_ref.id
    
    def create_recipe(self,name:str,description:str,ingredients: List[str],portions:List[str],diners:int,uid:str,image: UploadFile)->Recipe:
        recipe_service = RecipeService()
        self.categories = recipe_service.__calculate_categories(ingredients)
        public_url = recipe_service.__store_file(image)
        recipe = Recipe(
            name = name,
            description = description,
            ingredients = ingredients,
            portions = portions,
            diner = diners,
            created_by = uid,
            image = public_url,
            category = self.categories
        )
        return recipe
    
    def __store_file(self,file: UploadFile):
        unique_filename = f'{uuid.uuid4()}{os.path.splitext(file.filename)[1]}'
        bucket_name = os.getenv('STORAGE_BUCKET')
        bucket = storage.bucket(bucket_name)
        blob = bucket.blob(f'Img recetas/{unique_filename}')
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()
        return blob.public_url
    
    def __calculate_categories(self,new_recipes:List[str])->list|None:
        y = pd.read_pickle(self.current_directory + "/../resources/processed_y.pkl")
        with open(self.current_directory + "/../resources/modelo_recetas.pkl", 'rb') as f:
            multi_target_rf = pickle.load(f)
        with open(self.current_directory + "/../resources/vectorizer.pkl", 'rb') as f:
            vect = pickle.load(f)
        new_recipes_joined = ' '.join(new_recipes) 
        new_data_vectorized = vect.transform([new_recipes_joined])
        predictions = multi_target_rf.predict(new_data_vectorized)
        categories = []
        prediction = predictions[0]
        for category, is_set in zip(y.columns, prediction):
            if is_set:
                categories.append(category)
        return categories
    
    def get_all_recipes(self)->List[Dict[str,str]]:
        collection_ref = self.db.collection('Recetas')
        docs = list(collection_ref.stream())
        documents = []
        for doc in docs:
            recipe = doc.to_dict()
            for key,category in enumerate(recipe['category']):
                recipe['category'][key] = category.replace('Categoria_','')
            recipe['id'] = doc.id
            documents.append(recipe) 
        return documents
