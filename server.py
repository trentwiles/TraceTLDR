# converts the results into API format


from flask import Flask, request, jsonify
import db
import ai
import json

app = Flask(__name__)

# Welcome route
@app.route('/')
def home():
    return jsonify(message="OMG")

@app.route('/_api/getTeacherByID/<int:id>', methods=['GET'])
def get_data(id):
    id = int(id)
    return db.apiSelectTeacher(id)

@app.route('/_api/getTeacherSummary/<int:id>', methods=['GET'])
def get_summary(id):
    id = int(id)
    data = db.apiSelectTeacher(id)
    
    print(data)
    
    if data == {} or json.loads(data) == {}:
        return jsonify({"message": "Teacher not found"}), 404
    
    data = json.loads(data)
    
    goodString = ""
    badString = ""
    
    for goodComment in data["all_good_comments"]:
        goodString += goodComment + ", "
        
    for badComment in data["all_bad_comments"]:
        badString += badComment + ", "
        
    good = ai.summarize("positive", goodString)
    bad = ai.summarize("critical", badString)
    return jsonify({"positive": good, "critical": bad})

@app.route('/_api/searchTeacher/<q>', methods=['GET'])
def search(q):
    return db.searchTeacher(q)

# Start the server
if __name__ == '__main__':
    app.run(debug=True, port=5000)
