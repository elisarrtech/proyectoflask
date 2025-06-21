from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "tu_clave_secreta_aqui"

# Configurar base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar base de datos
db = SQLAlchemy(app)

# Modelos
class Chatbot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    idioma = db.Column(db.String(10), default='es')
    activo = db.Column(db.Boolean, default=True)
    respuesta_predeterminada = db.Column(db.String(300))
    faqs = db.relationship('FAQ', backref='chatbot', lazy=True)

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(300))
    respuesta = db.Column(db.String(500))
    chatbot_id = db.Column(db.Integer, db.ForeignKey('chatbot.id'), nullable=False)

# Rutas
@app.route("/")
def index():
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    chatbots = Chatbot.query.all()
    return render_template("dashboard.html", chatbots=chatbots)

@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        idioma = request.form.get("idioma", "es")
        activo = request.form.get("activo") == "on"
        respuesta_predeterminada = request.form.get("respuesta_predeterminada", "")

        nuevo_bot = Chatbot(
            nombre=nombre,
            descripcion=descripcion,
            idioma=idioma,
            activo=activo,
            respuesta_predeterminada=respuesta_predeterminada
        )
        db.session.add(nuevo_bot)
        db.session.commit()
        flash(f'Chatbot "{nombre}" creado con éxito.', "success")
        return redirect(url_for("dashboard"))
    return render_template("new_bot.html")

@app.route("/editar/<int:bot_id>", methods=["GET", "POST"])
def editar(bot_id):
    bot = Chatbot.query.get_or_404(bot_id)
    if request.method == "POST":
        bot.nombre = request.form["nombre"]
        bot.descripcion = request.form["descripcion"]
        bot.idioma = request.form.get("idioma", "es")
        bot.activo = request.form.get("activo") == "on"
        bot.respuesta_predeterminada = request.form.get("respuesta_predeterminada", "")
        db.session.commit()
        flash(f'Chatbot "{bot.nombre}" actualizado correctamente.', "success")
        return redirect(url_for("dashboard"))
    return render_template("edit_bot.html", bot=bot)

@app.route("/borrar", methods=["POST"])
def borrar():
    bot_id = int(request.form.get("bot_id"))
    bot = Chatbot.query.get(bot_id)
    if bot:
        db.session.delete(bot)
        db.session.commit()
        flash(f"Chatbot con ID {bot_id} borrado correctamente.", "danger")
    return redirect(url_for("dashboard"))

# FAQ management
@app.route("/faqs/<int:bot_id>")
def faqs(bot_id):
    bot = Chatbot.query.get_or_404(bot_id)
    return render_template("faqs.html", bot=bot, faqs=bot.faqs)

@app.route("/faqs/<int:bot_id>/nuevo", methods=["GET", "POST"])
def faq_nuevo(bot_id):
    bot = Chatbot.query.get_or_404(bot_id)
    if request.method == "POST":
        pregunta = request.form["pregunta"]
        respuesta = request.form["respuesta"]
        nueva_faq = FAQ(pregunta=pregunta, respuesta=respuesta, chatbot=bot)
        db.session.add(nueva_faq)
        db.session.commit()
        flash("FAQ agregada correctamente.", "success")
        return redirect(url_for("faqs", bot_id=bot_id))
    return render_template("new_faq.html", bot=bot)

@app.route("/faqs/<int:bot_id>/editar/<int:faq_id>", methods=["GET", "POST"])
def faq_editar(bot_id, faq_id):
    bot = Chatbot.query.get_or_404(bot_id)
    faq = FAQ.query.get_or_404(faq_id)
    if request.method == "POST":
        faq.pregunta = request.form["pregunta"]
        faq.respuesta = request.form["respuesta"]
        db.session.commit()
        flash("FAQ actualizada correctamente.", "success")
        return redirect(url_for("faqs", bot_id=bot_id))
    return render_template("edit_faq.html", bot=bot, faq=faq)

@app.route("/faqs/<int:bot_id>/borrar/<int:faq_id>", methods=["POST"])
def faq_borrar(bot_id, faq_id):
    faq = FAQ.query.get_or_404(faq_id)
    db.session.delete(faq)
    db.session.commit()
    flash("FAQ borrada correctamente.", "danger")
    return redirect(url_for("faqs", bot_id=bot_id))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)

