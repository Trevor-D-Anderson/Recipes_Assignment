from flask_app.config.mysqlconnection import connectToMySQL

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.recipe_name = data['recipe_name']
        self.under_30 = data['under_30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_recipe(cls, data):
        query = "insert into recipes (recipe_name, under_30, description, instructions, user_id) values(%(recipe_name)s, %(under_30)s, %(description)s, %(instructions)s, %(user_id)s)"
        return connectToMySQL("recipes_schema").query_db(query, data)

    @classmethod
    def get_recipes(cls, id):
        query = "select * from recipes join users on users.id = recipes.user_id where user_id = %(id)s"
        results = connectToMySQL("recipes_schema").query_db(query, id)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "select * from recipes join users on users.id = recipes.user_id where user_id = %(user_id)s and recipes.id = %(id)s"
        result = connectToMySQL("recipes_schema").query_db(query, data)
        recipes = []
        for recipe in result:
            recipes.append(cls(recipe))
        return recipes[0]

    @classmethod
    def edit_recipe(cls, data):
        query = "update recipes set recipe_name = %(recipe_name)s, under_30 = %(under_30)s, description = %(description)s, instructions = %(instructions)s where id = %(recipes.id)s"
        return connectToMySQL("recipes_schema").query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = "delete from recipes where id = %(recipe_id)s"
        return connectToMySQL("recipes_schema").query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['recipe_name']) <4:
            flash("Recipe name must be at least 3 characters")
            is_valid = False
        if len(recipe['description']) <4:
            flash("Description must be at least 3 characters")
            is_valid = False
        if len(recipe['instructions']) <4:
            flash("Instructions must be at least 3 characters")
            is_valid = False
        return is_valid
