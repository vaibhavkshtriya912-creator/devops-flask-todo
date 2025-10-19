import os, json
from uuid import uuid4
from hashlib import sha256
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "todoapp")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "items")

def get_collection():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1500)
        client.server_info()
        return client[DB_NAME][COLLECTION_NAME]
    except Exception:
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=["GET"])
def api():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": "data.json missing/invalid", "details": str(e)}), 500

# route to store to-do in MongoDB

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get("itemName")
    desc = data.get("itemDescription")
    item_id = data.get("itemId")
    item_uuid = data.get("itemUuid")
    item_hash = data.get("itemHash")

    if not name or not desc:
        return jsonify({"ok": False, "error": "itemName and itemDescription are required"}), 400

    if not item_uuid:
        item_uuid = str(uuid4())
    if not item_hash:
        item_hash = sha256(f"{name}:{desc}".encode("utf-8")).hexdigest()

    doc = {
        "itemName": name,
        "itemDescription": desc,
        "itemId": item_id,
        "itemUuid": item_uuid,
        "itemHash": item_hash,
    }

    coll = get_collection()
    if coll is None:
        with open("submitted_items_fallback.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(doc) + "\n")
        return jsonify({"ok": True, "stored": "file", "doc": doc}), 201

    inserted = coll.insert_one(doc)
    return jsonify({"ok": True, "stored": "mongodb", "id": str(inserted.inserted_id), "doc": doc}), 201

if __name__ == "__main__":
    app.run(debug=True)
