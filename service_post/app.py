from flask import Flask, jsonify, request, abort
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models_shared.models import Base, User, Post

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@app.before_first_request
def create_tables():
    Base.metadata.create_all(bind=engine)

@app.route("/posts", methods=["GET"])
def get_posts():
    session = SessionLocal()
    posts = session.query(Post, User).join(User, Post.user_id == User.id).all()
    result = []
    for post, user in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "username": user.username
        })
    session.close()
    return jsonify(result)

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    if not data.get("title") or not data.get("content") or not data.get("user_id"):
        abort(400)
    session = SessionLocal()
    u = session.query(User).get(data["user_id"])
    if not u:
        session.close()
        abort(400, description="user_id not found")
    new = Post(title=data["title"], content=data["content"], user_id=data["user_id"])
    session.add(new)
    session.commit()
    session.refresh(new)
    res = {
        "id": new.id,
        "title": new.title,
        "content": new.content,
        "user_id": new.user_id
    }
    session.close()
    return jsonify(res), 201

@app.route("/posts/by_user", methods=["GET"])
def get_posts_by_user():
    user_id = request.args.get("user_id", type=int)
    session = SessionLocal()
    q = session.query(Post, User).join(User, Post.user_id == User.id)
    if user_id:
        q = q.filter(Post.user_id == user_id)
    posts = q.all()
    result = []
    for post, user in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "user_id": post.user_id,
            "username": user.username
        })
    session.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
