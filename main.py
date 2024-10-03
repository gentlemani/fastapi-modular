from fastapi import FastAPI, Form, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from services.recipeService import RecipeService
from services.firebaseAuth import FirebaseAuth

from services.recommendationService import RecommendationService
import json
app = FastAPI()

auth_service = FirebaseAuth()
prefix = "/api/v1"
@app.post(prefix + "/recipe")
async def create_recipe(
    image: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    ingredients: str = Form(..., example=["pasta", "tomato sauce", "cheese"]),
    portions: str = Form(...,example=["200gr", "1l", "Una pizca"]),
    diners: int = Form(...),
    decoded_token=Depends(auth_service.verify_firebase_token)
):
    recipe_service = RecipeService()
    recipe = recipe_service.create_recipe(name,description,json.loads(ingredients),json.loads(portions),diners,
                                        decoded_token.get('uid'),image)
    recipe_id = recipe_service.store_recipe(recipe)
    categories = recipe_service.get_categories()
    return JSONResponse(
        status_code=201,
        content={
            "message": "Recipe created",
            "recipe_id": recipe_id,
            "Categories": categories,
        }
    )

@app.get(prefix + "/recommendation")
async def get_recommendations(decoded_token=Depends(auth_service.verify_firebase_token)):
    recommendation_service = RecommendationService()
    recommendations = recommendation_service.get_recommendation(decoded_token.get('uid'))
    return JSONResponse(
        status_code=200,
        content={
            "message": "Recipe created",
            "recommendations":recommendations
        }
    )
    
@app.get(prefix + "/category")
async def create_recipe(
    ingredients: str = Form(..., example=["pasta", "tomato sauce", "cheese"]),
    decoded_token=Depends(auth_service.verify_firebase_token)
):
    recipe_service = RecipeService()
    categories = recipe_service.calculate_categories(json.loads(ingredients))
    return JSONResponse(
        status_code=201,
        content={
            "message": "Recipe created",
            "Categories": categories,
        }
    )