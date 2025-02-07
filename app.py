from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from routes.auth_routes import auth_bp
from routes.library_routes import library_bp
from routes.forum_routes import forum_bp
from routes.comment_routes import comment_bp
from routes.exam_routes import exam_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = config.SECRET_KEY
jwt = JWTManager(app)

CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(library_bp)
app.register_blueprint(forum_bp)
app.register_blueprint(comment_bp)
app.register_blueprint(exam_bp)

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
if __name__ == "__main__":
    app.run(debug=True)
