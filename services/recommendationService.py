import pandas as pd
from sklearn.cluster import KMeans
# import joblib
from typing import List, Dict
from services.userService import UserService
from services.recipeService import RecipeService

class RecommendationService:
    def __init__(self) -> None:
        recipe_service = RecipeService()
        self.recipes = recipe_service.get_all_recipes()
        users_service = UserService()
        self.users = users_service.get_all_users()
        
    def get_recommendation(self,user_id:str,top_n: int = None)->list:
        """Get recommendations for a user.

        Args:
            user_id (str): User identifier.
            top_n (int, optional): Máximum number of recipes to retreive. Defaults to None.

        Returns:
            list: Returns the recommendations obtained.
        """
        return self.__recipe_recommendation_kmeans(user_id,self.users,self.recipes,top_n)
        
    def __calculate_puntuation(self, recipe: dict, preferences: pd.Series) -> int:
        """Gets the puntuation of every recipe.

        Args:
            recipe (dict): A dictionary with the categories of the recipes. 
            preferences (pd.Series): Preferenses of the user

        Returns:
            int: Returns a number that will be the score obtained
        """
        puntuacion = 0
        for category in recipe.get('category', []):
            puntuacion += preferences.get(category, 0)
        return puntuacion

    def __recipe_recommendation_kmeans(self,user_id:str,users: Dict[str,Dict[str,int]], recipes: List[Dict[str,str]],top_n: int = None) -> list:
        """Recommend certain recipes based on the user frecuency table, other users and the recipes availables.

        Args:
            user_id (str): User identificator.
            users (Dict[str,Dict[str,str]]): All users to compare to. The key must be the id of the user.
            recipes (dict): recipes, It must have some key values like `name`, `id`, and `category`.
            top_n (int, optional): Number of maximum options to be listed. Defaults to None.

        Returns:
            list: Returns all the recomedations obtained.
        """
        #To prevent problems with variables
        if user_id not in users:
            return []
        """
        T parameter means transposing
        Example without T
                User_1  User_2
        Meat      2        1
        Fruits    3        5
        Dairy     5        0
        
        With T parameter
                Meat Fruits Dairy
        User_1   2     3      5
        User_2   1     5      0
        """
        data = pd.DataFrame(users).T
        data.fillna(0, inplace=True)

        kmeans = KMeans(n_clusters=5, random_state=0)
        data['cluster'] = kmeans.fit_predict(data)

        # joblib.dump(kmeans, 'kmeans_model.pkl')
        
        user_cluster = data.loc[user_id, 'cluster']

        cluster_preferences = data[data['cluster'] == user_cluster].drop('cluster', axis=1).mean()
        categorias_excluir = [cat for cat, val in cluster_preferences.items() if val < 0]

        filtered_recipes = [
            recipe for recipe in recipes
            if not any(cat in categorias_excluir for cat in recipe.get('category', [])) and (not recipe.get('created_by') or recipe.get('created_by') == user_id)
        ]

        if not filtered_recipes:
            print(f"No hay recetas disponibles para {user_id} después de aplicar las exclusiones de clustering.")
            return []

        rated_recipes = [
            {
                'id': recipe['id'],
                'name': recipe.get('name', 'No name'),
                'puntuation': self.__calculate_puntuation(recipe, cluster_preferences)
            }
            for recipe in filtered_recipes
        ]

        sort_recipes = sorted(rated_recipes, key=lambda x: x['puntuation'], reverse=True)
        if(top_n):
            return sort_recipes[:top_n]
        else:
            return sort_recipes

    def show_kmeans_recommendations(self,recommendations: list, user_id:str) -> None:
        """Prints in console the result obtained for a particular user.

        Args:
            recommendations (list): Receipes previously recommended for the user.
            user_id (str): User identificator. Just to print it.
        """
        if recommendations:
            print(f"\nRecetas recomendadas para {user_id} basadas en clustering de preferencias:")
            for recipe in recommendations:
                print(f" - {recipe['name']} (Puntuación: {recipe['puntuation']})")
        else:
            print(f"\nNo se encontraron recomendaciones para {user_id}.")
            