# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import session,flash

class Cookie:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cookie_type = data['cookie_type']
        self.num_of_boxes = data['num_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cookie_orders;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('cookies').query_db(query)
        # Create an empty list to append our instances of orders
        orders = []
        # Iterate over the db results and create instances of orders with cls.
        for order in results:
            orders.append(cls(order))
        return orders

    @classmethod
    def save(cls, data):
        query = "INSERT INTO cookie_orders ( name , cookie_type, num_of_boxes , created_at, updated_at ) VALUES ( %(name)s , %(cookie_type)s , %(num_of_boxes)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        result = connectToMySQL('cookies').query_db(query, data)
        return result

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM cookie_orders WHERE id = %(id)s;"
        data = {
            "id" : id
        }
        result = connectToMySQL('cookies').query_db(query, data)
        if result:
            order = result[0]
            return order
        return False

    @classmethod
    def update(cls, data):
        query = "UPDATE cookie_orders SET name = %(name)s, cookie_type = %(cookie_type)s, num_of_boxes = %(num_of_boxes)s, updated_at = NOW() WHERE id = %(id)s;"
        result = connectToMySQL('cookies').query_db(query, data)
        return result

    @staticmethod
    def validate_user(cookies):
        is_valid = True  # we assume this is true
        if len(cookies['name']) < 2:
            flash("First name is required.", "error")
            is_valid = False
        if len(cookies['cookie_type']) < 2:
            flash("Cookie type is required.", "error")
            is_valid = False
        if int(cookies['num_of_boxes']) <= 0:
            flash("Please enter a valid number of boxes.", "error")
            is_valid = False
        return is_valid