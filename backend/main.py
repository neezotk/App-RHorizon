from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
from .config import settings
from .db import init_db, db_healthcheck, insert_item, list_items
from .s3_utils import s3_healthcheck, upload_fileobj

app = Flask(__name__)
CORS(app)

with app.app_context():
    init_db()

@app.get("/api")
def hello():
    return jsonify({"message": "Hello from RHorizon backend!", "version": 2})

@app.get("/api/health")
def health():
    db_ok, db_err = db_healthcheck()
    s3_ok, s3_err = s3_healthcheck()
    status = "ok" if db_ok and s3_ok else "degraded"
    return jsonify({
        "status": status,
        "db": {"ok": db_ok, "error": db_err},
        "s3": {"ok": s3_ok, "error": s3_err}
    }), (200 if status == "ok" else 503)

@app.post("/api/items")
def create_item():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    insert_item(name)
    return jsonify({"ok": True}), 201

@app.get("/api/items")
def get_items():
    return jsonify(list_items())

@app.post("/api/upload")
def upload():
    """Upload a file to S3 bucket specified by S3_BUCKET_NAME."""
    if "file" not in request.files:
        return jsonify({"error": "file is required"}), 400
    f = request.files["file"]
    key = f"uploads/{uuid.uuid4().hex}-{secure_filename(f.filename)}"
    meta = upload_fileobj(f.stream, key, f.mimetype or "application/octet-stream")
    return jsonify(meta), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=settings.DEBUG)
