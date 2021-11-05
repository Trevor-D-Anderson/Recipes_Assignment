from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re	# the regex module
# create a regular expression object that we'll use later   
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z]).{2,16}$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, username, password) VALUES(%(first_name)s, %(last_name)s, %(username)s, %(password)s)"
        return connectToMySQL("recipes_schema").query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes_schema').query_db(query)
        users = []
        for user in results:
            users.append( User(user) )
        return users

    @classmethod
    def delete_user(cls, id):
        query = "DELETE FROM users WHERE id=%(id)s"
        return connectToMySQL("recipes_schema").query_db(query,id)
    
    @classmethod
    def show_user(cls, id):
        query = "SELECT * FROM users WHERE id=%(id)s"
        return connectToMySQL("recipes_schema").query_db(query,id)

    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, username = %(username)s where id =%(id)s"
        return connectToMySQL("recipes_schema").query_db(query,data)

    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL("recipes_schema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) <3:
            flash("Name must be at least 2 characters")
            is_valid = False
        if len(user['last_name']) <3:
            flash("Last name must be at least 2 characters")
            is_valid = False
        if len(user['username']) <3:
            flash("Username must be at least 2 characters")
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']): 
            flash("Invalid Password! Must include 1 capital letter and 1 number.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords Must Match")
            is_valid = False
        return is_valid
