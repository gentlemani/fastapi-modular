from fastapi import FastAPI, Form, UploadFile, File, Depends
from services.recipeService import RecipeService
from services.firebaseAuthClass import FirebaseAuth
from models.recipe import Recipe
from typing import List

app = FastAPI()

auth_service = FirebaseAuth()

@app.post("/secure-endpoint")
async def secure_endpoint(
    image: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(...),
    ingredients: List[str] = Form(...),
    portions: List[str] = Form(...),
    # decoded_token=Depends(auth_service.verify_firebase_token)
):
    
    # Use the RecipeService to handle the file upload
    recipe_service = RecipeService()
    public_url = recipe_service.store_file(image)
    recipe = Recipe(
        name=name,
        description=description,
        ingredients=ingredients,
        portions=portions,
        image=public_url
    )
    categories = recipe_service.get_category(recipe.ingredients)
    recipe.category = categories
    recipe_service.store_recipe(recipe)
    # email = decoded_token.get('email')
    return {
        # "message": "Hello, {email}!",
        "Categories": categories,
        "image_url": public_url  # Optionally return the image URL
    }
