from flask_app.config.mysqlconnection import connectToMySQL
import re  # the regex module
from flask import flash
# create a regular expression object that we'll use later


class Show:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['title']
        self.description = data['network']
        self.instructions = data['description']
        self.dateMade = data['release_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    # Now we use class methods to query our database

    db_name = 'finalexamcd'

    @classmethod
    def get_show_by_id(cls, data):
        query = 'SELECT * FROM shows WHERE id= %(show_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def getUserWhoLikedshows(cls, data):
        query = "SELECT likes.user_id as id from likes WHERE show_id = %(show_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        likes = []
        if results:
            for like in results:
                likes.append(like['id'])
            return likes
        return likes

    @classmethod
    def get_all(cls):
        query = "SELECT shows.id as id, shows.title as title, shows.network as network, shows.release_date as release_date, shows.network as network, shows.user_id as user_id, COUNT(likes.id) as likes FROM shows LEFT JOIN users on shows.user_id = users.id LEFT JOIN likes on likes.show_id =shows.id GROUP BY shows.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        shows = []
        if results:
            for show in results:
                shows.append(show)
            return shows
        return shows

    @classmethod
    def showCreator(cls, data):
        query = "SELECT shows.id AS show_id, shows.user_id, users.id AS user_id, users.first_name as first_name, users.last_name as last_name FROM shows LEFT JOIN users ON shows.user_id = users.id WHERE shows.id = %(show_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if result:
            return result[0]
        return False

    @classmethod
    def getShowLikes(cls, data):
        query = "SELECT COUNT(DISTINCT likes.user_id) AS total_likes FROM likes WHERE likes.show_id = %(show_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def create_show(cls, data):
        query = "INSERT INTO shows (title, network, description, release_date, user_id) VALUES ( %(title)s, %(network)s,  %(description)s, %(release_date)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes (user_id, show_id) VALUES ( %(user_id)s, %(show_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND show_id = %(show_id)s"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_show(cls, data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE id = %(show_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_show_likes(cls, data):
        query = "DELETE from likes WHERE show_id = %(show_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id = %(show_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_show(r):
        is_valid = True
        if not r['title']:
            flash('Title field is required', 'title')
            is_valid = False
        if not r['network']:
            flash('Network field is required', 'network')
            is_valid = False
        if not r['release_date']:
            flash('Release date is required', 'release_date')
            is_valid = False
        if len(r['description']) < 3:
            flash('Description must be more than 3 characters', 'description')
            is_valid = False
        return is_valid
