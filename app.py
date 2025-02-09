from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from routes.auth_routes import auth_bp
from routes.library_routes import library_bp
from routes.forum_routes import forum_bp
from routes.comment_routes import comment_bp
from routes.exam_routes import exam_bp
from routes.message_routes import mess_bp
from routes.minigame_routes import minigame_bp
from models.message import MessageModel
from datetime import datetime
from flask_pymongo import PyMongo  
from flask_socketio import SocketIO, emit, join_room, leave_room
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = config.SECRET_KEY
jwt = JWTManager(app)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
mongo = PyMongo()
app.config["MONGO_CLIENT"] = mongo
app.register_blueprint(auth_bp)
app.register_blueprint(library_bp)
app.register_blueprint(forum_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(exam_bp)
app.register_blueprint(mess_bp)
app.register_blueprint(minigame_bp)



@socketio.on("join")
def handle_join(data):
    """ Người dùng tham gia phòng chat """
    user = data.get("user")
    room = data.get("room")
    join_room(room)
    emit("user_joined", {"user": user, "room": room}, room=room)

@socketio.on("leave")
def handle_leave(data):
    """ Người dùng rời phòng chat """
    user = data.get("user")
    room = data.get("room")
    leave_room(room)
    emit("user_left", {"user": user, "room": room}, room=room)

@socketio.on("send_message")
def handle_send_message(data):
    """ Khi người dùng gửi tin nhắn """
    user = data.get("user")
    message = data.get("message")
    room = data.get("room")
    timestamp = data.get("timestamp")  

    if timestamp:
        timestamp_dt = datetime.strptime(timestamp.replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S.%f")
        formatted_timestamp = timestamp_dt.strftime("%H:%M %d/%m/%Y")
    else:
        formatted_timestamp = "Không có thời gian"

    msg = MessageModel.save_message(user, message, room)

    emit("new_message", {
        "user": msg["user"],
        "message": msg["message"],
        "timestamp": formatted_timestamp
    }, room=room)

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/minigame")
def minigame():
    return render_template("minigame.html")

@app.route('/login')
def login():
    return render_template("auth.html")

@app.route('/lib')
def library():
    return render_template("library.html")

@app.route('/forum')
def diendan():
    return render_template("diendan.html")

@app.route('/dethi')
def dethi():
    return render_template("dethi.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/qldiendan')
def qldiendan():
    return render_template("quanlydiendan.html")
@app.route('/qlnguoidung')
def qlnguoidung():
    return render_template("quanlynguoidung.html")
@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

@app.route('/lienhe')
def lienhe():
    return render_template("lienhe.html")
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)

