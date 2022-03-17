from app.config.mysqlconnection import connectToMySQL
from flask import flash, request

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Email:
    db = 'email_validation'
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def validate_email( email ):
        is_valid = True
        # test whether user added input
        if len(email['email']) < 1:
            flash("Please input an email address!")
            is_valid = False
        #test if email matches email pattern
        elif not EMAIL_REGEX.match(email['email']): 
            flash("Invalid email address format!")
            is_valid = False
        #test whether the email already exists
        query = "SELECT * FROM email WHERE email = %(email)s;"
        results = connectToMySQL(Email.db).query_db(query, email)
        if len(results) >=1:
            flash("That email already exists in the database!")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM email;"
        results = connectToMySQL(cls.db).query_db(query)
        emails = []
        for e in results:
            emails.append(cls(e))
        return emails
    
    @classmethod
    def get_one(cls, data):
            query = "SELECT * FROM email WHERE id = %(id)s;"
            results = connectToMySQL(cls.db).query_db(query, data)
            if len(results) < 1:
                return False
            return cls(results[0])
        
    @classmethod
    def insert(cls, data):
        query = "INSERT INTO email (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update(cls, data):
        query = "UPDATE email SET email=%(email)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM email WHERE email=%(email)s LIMIT 1;"
        return connectToMySQL(cls.db).query_db(query, data)