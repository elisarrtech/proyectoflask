
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Página de inicio (login falso por ahora)
@app.route("/")
def index():
    return render_template("index.html")

# Dashboard principal
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Crear un nuevo chatbot
@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        # Aquí guardarás a base de datos más adelante
        return redirect(url_for("dashboard"))
    return render_template("new_bot.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
