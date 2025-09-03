from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection (adjust URI if needed)
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["todos"]

# --- Form Page ---
@app.route("/", methods=["GET", "POST"])
def index():
    error_message = None
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            error_message = "Both fields are required."
        else:
            try:
                collection.insert_one({"name": name, "email": email})
                return redirect(url_for("success"))
            except Exception as e:
                error_message = str(e)

    return render_template("index.html", error=error_message)

@app.route("/success")
def success():
    return render_template("success.html")

# API route with JSON file data
import json
@app.route("/api")
def api():
    with open("data.json") as f:
        data = json.load(f)
    return jsonify(data)

# Backend route for To-Do items
@app.route("/submittodoitem", methods=["POST"])
def submit_todo():
    data = request.json
    db.todo.insert_one({
        "itemId": data.get("itemId"),
        "itemUUID": data.get("itemUUID"),
        "itemHash": data.get("itemHash"),
        "itemName": data.get("itemName"),
        "itemDescription": data.get("itemDescription")
    })
    return {"status": "success"}

if __name__ == "__main__":
    app.run(debug=True)
