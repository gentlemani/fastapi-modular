from fastapi import FastAPI, Form, UploadFile, File, Depends,HTTPException
from fastapi.responses import JSONResponse
from services.recipeService import RecipeService
from services.firebaseAuthClass import FirebaseAuth
from models.recipe import Recipe
from typing import List

app = FastAPI()

auth_service = FirebaseAuth()

@app.post("/recipe")
async def secure_endpoint(
    image: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    ingredients: List[str] = Form(...),
    portions: List[str] = Form(...),
    decoded_token=Depends(auth_service.verify_firebase_token)
):
    
    # Use the RecipeService to handle the file upload
    recipe_service = RecipeService()
    categories = recipe_service.get_category(ingredients)
    if categories is None:
        raise HTTPException(status_code=400, detail="The provided ingredients do not match the required ones.")
    public_url = recipe_service.store_file(image)
    recipe = Recipe(
        name=name,
        description=description,
        ingredients=ingredients,
        portions=portions,
        image=public_url
    )
    recipe.category = categories
    recipe_service.store_recipe(recipe)
    email = decoded_token.get('email')
    return JSONResponse(
        status_code=201,
        content={
            "message": f"Hello, {email}!",
            "Categories": categories,
        }
    )
