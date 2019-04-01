from chalice import Chalice, Response
from chalice import BadRequestError
from chalice import NotFoundError

from chalicelib import db_connect

import logging
import json

app = Chalice(app_name='toys')
app.debug = True
             
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# GET all users
@app.route("/users", methods=['GET'])
def users():
    result = []
    with db_connect.conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        row_headers = [x[0] for x in cur.description]
        for row in cur:
            result.append(dict(zip(row_headers, row)))
        print(result)
    response = {
        "statusCode": 200,
        "body": result
    }
    return response

# GET a user 
@app.route("/users/{user_id}", methods=['GET'])
def get_user_info(user_id):
    result = []
    with db_connect.conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE user_id = %s", user_id)
        row_headers = [x[0] for x in cur.description]
        for row in cur:
            result.append(dict(zip(row_headers, row)))
        print(result)
    response = {
        "statusCode": 200,
        "body": result
    }
    return response

# CREATE a user
@app.route("/users", methods=['POST'])
def create_user():
    try:
        user_add = app.current_request.json_body
        with db_connect.conn.cursor() as cur:
            sql_query = "INSERT INTO users(email, user_name, age, gender) VALUES('%s', '%s', %d, '%s')" % (user_add['email'], user_add['user_name'], user_add['age'], user_add['gender'])
            print(sql_query)
            cur.execute(sql_query)
            db_connect.conn.commit()
            cur.close()
        return json.dumps("Add Success!")
    except:
        db_connect.conn.rollback()

# UPDATE a user
@app.route("/users/{user_id}", methods=['PUT'])
def update_user(user_id):
    user_update = app.current_request.json_body
    print(user_update)
    print(user_id)
    with db_connect.conn.cursor() as cur:
        for key, value in user_update.items():
            sql_query = "UPDATE users SET %s = '%s' where user_id = %s" % (key, value, user_id)
            print(sql_query)
            cur.execute(sql_query)
        db_connect.conn.commit()
        cur.close()
    return json.dumps("Update Success!")

# UPDATE a user
# @app.route("/users/{user_id}", methods=['PUT'])
# def update_user(user_id):
#     user_update = app.current_request.json_body
#     with db_connect.conn.cursor() as cur:
#         sql_query = "UPDATE users SET email='%s', user_name='%s', age='%d', gender='%s' where user_id=%s" % (user_update['email'], user_update['user_name'], user_update['age'], user_update['gender'], user_id)
#         print(sql_query)
#         cur.execute(sql_query)
#         db_connect.conn.commit()
#         cur.close()
#     return json.dumps("Update Success!")
    
