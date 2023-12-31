from flask import Flask, request
from flask_cors import CORS
import evadb

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})
    
cursor = evadb.connect().cursor()


@app.route('/execute', methods = ['POST'])
def execute():
    data = request.json['query']
    res = cursor.query(data).df()
    return res.to_json(orient ='records')

@app.route('/create', methods = ['POST'])
def create():
    data = request.json['params']
    query = """
        CREATE DATABASE {name}
        WITH ENGINE = '{engine}',
        PARAMETERS = {{
            "user": '{user}',
            "password": '{password}',
            "host": '{host}',
            "port": '{port}',
            "database": '{db}'
        }};
    """.format(name=data['name'], engine=data['engine'], user=data['user'], password=data['password'], host=data['host'], port=data['port'], db=data['db'])
    res = cursor.query(query).df()
    return res.to_json(orient ='records')

def run():
    return app


if __name__ == "__main__":
    app.run(debug=True)         
