from fastapi import FastAPI, Request, UploadFile,File
from services.recipeService import RecipeService
from services.firebaseAuthClass import FirebaseAuth
from firebase_admin import firestore
from models.recipe import Recipe
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import json

app = FastAPI()

auth_service = FirebaseAuth()
db = firestore.client()
@app.post("/secure-endpoint")
async def secure_endpoint(
    request: Request,
    image:UploadFile = File(...)
    # decoded_token=Depends(auth_service.verify_firebase_token)
    ):
    body = await request.body()
    if not body:
        return JSONResponse(
            status_code=422,
            content={"detail": "The request body is empty. Please provide required fields."}
        )

    try:
        # Decode the JSON
        data = json.loads(body)
        recipe = Recipe(**data)
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=422,
            content={"detail": "Invalid JSON. Please ensure the request body is properly formatted."}
        )
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"detail": e.errors()}
        )
    
    # uid = decoded_token.get('email')
    recipe_service = RecipeService()
    public_url = recipe_service.store_file(image)
    print(public_url)
    categories = recipe_service.get_category(recipe.ingredients)
    return {
        "message": f"Hello, user !",
        "Categories": categories
    }

