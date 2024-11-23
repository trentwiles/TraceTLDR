# converts the results into API format


from flask import Flask, request, jsonify
import db

app = Flask(__name__)

# Welcome route
@app.route('/')
def home():
    return jsonify(message="OMG")

@app.route('/_api/getTeacherByID/<int:id>', methods=['GET'])
def get_data(id):
    id = int(id)
    return db.apiSelectTeacher(id)

@app.route('/_api/searchTeacher/<q>', methods=['GET'])
def search(q):
    return db.searchTeacher(q)

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
