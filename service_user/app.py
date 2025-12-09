from flask import Flask, jsonify, request, abort
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_shared.models import Base, User

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@app.before_first_request
def create_tables():
    Base.metadata.create_all(bind=engine)

@app.route("/users", methods=["GET"])
def get_users():
    session = SessionLocal()
    users = session.query(User).all()
    result = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    session.close()
    return jsonify(result)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("username") or not data.get("email"):
        abort(400)
    session = SessionLocal()
    new = User(username=data["username"], email=data["email"])
    session.add(new)
    session.commit()
    session.refresh(new)
    res = {"id": new.id, "username": new.username, "email": new.email}
    session.close()
    return jsonify(res), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    session = SessionLocal()
    u = session.query(User).get(user_id)
    session.close()
    if not u:
        abort(404)
    return jsonify({"id": u.id, "username": u.username, "email": u.email})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
