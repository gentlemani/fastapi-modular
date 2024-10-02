from fastapi import FastAPI, Form, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from services.recipeService import RecipeService
from services.firebaseAuth import FirebaseAuth
from models.recipe import Recipe
import json
app = FastAPI()

auth_service = FirebaseAuth()
prefix = "/api/v1"
@app.post(prefix + "/recipe")
async def secure_endpoint(
    image: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    ingredients: str = Form(..., example=["pasta", "tomato sauce", "cheese"]),
    portions: str = Form(...),
    diners: int = Form(...),
    decoded_token=Depends(auth_service.verify_firebase_token)
):
    ingredients_list = json.loads(ingredients)
    portions_list = json.loads(portions)
    recipe_service = RecipeService()
    categories = recipe_service.get_category(ingredients_list)
    public_url = recipe_service.store_file(image)
    recipe = Recipe(
        name = name,
        description = description,
        ingredients = ingredients_list,
        portions = portions_list,
        image = public_url,
        diner = diners,
        created_by = decoded_token.get('uid')
    )
    recipe.category = categories
    recipe_id = recipe_service.store_recipe(recipe)
    return JSONResponse(
        status_code=201,
        content={
            "message": "Recipe created",
            "recipe_id": recipe_id,
            "Categories": categories,
        }
    )
