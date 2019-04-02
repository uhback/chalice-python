from chalice import Chalice, Response
from chalice import BadRequestError
from chalice import NotFoundError

from chalicelib import db_connect

import logging
import json
import datetime

app = Chalice(app_name='toys')
app.debug = True
             
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Convert Date Time to String ("datetime.datetime(2016, 4, 8, 11, 43, 54, 920632)")
def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# GET all users
@app.route("/users", methods=['GET'])
def users():
    result = []
    with db_connect.conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        row_headers = [x[0] for x in cur.description]
        for row in cur:
            result.append(dict(zip(row_headers, row)))
    return json.dumps(result, default=datetime_converter)
    # return Response(body=result,
    #                 status_code=200,
    #                 headers={'Content-Type': 'application/json'})

# GET a user 
@app.route("/users/{user_id}", methods=['GET'])
def get_user_info(user_id):
    result = []
    with db_connect.conn.cursor() as cur:
        cur.execute("SELECT email, user_name, age, gender FROM users WHERE user_id = %s", user_id)
        row_headers = [x[0] for x in cur.description]
        for row in cur:
            result.append(dict(zip(row_headers, row)))
    return json.dumps(result, default=datetime_converter)
    # return Response(body=result,
    #                 status_code=200,
    #                 headers={'Content-Type': 'application/json'})

# CREATE a user
@app.route("/users", methods=['POST'])
def create_user():
    user_add = app.current_request.json_body
    with db_connect.conn.cursor() as cur:
        sql_query = "INSERT INTO users(email, user_name, age, gender) VALUES('%s', '%s', %d, '%s')" % (user_add['email'], user_add['user_name'], user_add['age'], user_add['gender'])
        cur.execute(sql_query)
        db_connect.conn.commit()
        cur.close()
    return Response(body='Complete',
                    status_code=200,
                    headers={'Content-Type': 'application/plain'})

# UPDATE a user
@app.route("/users/{user_id}", methods=['PUT'])
def update_user(user_id):
    user_update = app.current_request.json_body
    with db_connect.conn.cursor() as cur:
        for key, value in user_update.items():
            sql_query = "UPDATE users SET %s = '%s' where user_id = %s" % (key, value, user_id)
            print(sql_query)
            cur.execute(sql_query)
        db_connect.conn.commit()
        cur.close()
    return Response(body='Complete',
                    status_code=200,
                    headers={'Content-Type': 'application/plain'})