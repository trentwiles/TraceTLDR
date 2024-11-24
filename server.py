# converts the results into API format


from flask import Flask, Response, jsonify, render_template
import db
import ai
import json
import rmp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", title="Home")

@app.route('/teacher/<int:id>')
def teacher(id):
    return render_template("view.html", id=id, title="Teacher")

@app.route('/how-it-works')
def works():
    return render_template("how.html", title="How it Works")

@app.route('/_api/getTeacherByID/<int:id>', methods=['GET'])
def get_data(id):
    id = int(id)
    return Response(db.apiSelectTeacher(id), content_type="application/json")

@app.route('/_api/getTeacherSummary/<int:id>', methods=['GET'])
def get_summary(id):
    id = int(id)
    data = db.apiSelectTeacher(id)
        
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
    return Response(json.dumps(db.searchTeacher(q)), content_type="application/json")

# not implemented on frontend, far too slow
@app.route('/_api/rmpBackend/<q>')
def rate(q):
    return Response(json.dumps(rmp.getRating(q)), content_type="application/json")

# Start the server
if __name__ == '__main__':
    app.run(debug=False, port=5000)
